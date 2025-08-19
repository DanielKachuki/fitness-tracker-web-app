from django.contrib.auth.models import User
from django.db import connection
from django.db.models import Q
from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import WorkoutType, Workout, ScheduledWorkout, Goal
from .serializer import (
    UserSerializer,
    WorkoutTypeSerializer,
    WorkoutSerializer,
    ScheduledWorkoutSerializer,
    GoalSerializer,
    ProfileSerializer,
)

# ---------------------------
# Helpers
# ---------------------------

STATUS_CHOICES = {"scheduled", "completed", "missed", "canceled", "rescheduled"}  # DB ENUM

def _uid(request):
    """
    Map Django auth user -> DB Users.userID.
    If you store this mapping on a Profile model, return that instead.
    """
    # Example: if your Profile has a db_user_id field:
    if hasattr(request.user, "profile") and getattr(request.user.profile, "db_user_id", None):
        return request.user.profile.db_user_id
    # Fallback (only if you've aligned auth and DB user ids 1:1)
    return request.user.id

def dictfetchall(cursor):
    cols = [c[0] for c in cursor.description]
    return [dict(zip(cols, row)) for row in cursor.fetchall()]

# ---------------------------
# Auth / Profile
# ---------------------------

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated])
def profile_detail(request):
    profile = request.user.profile
    if request.method == "GET":
        return Response(ProfileSerializer(profile).data)
    serializer = ProfileSerializer(profile, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

# ---------------------------
# Workout Types (read-only)
# ---------------------------

class WorkoutTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WorkoutType.objects.all().order_by("workoutname")
    serializer_class = WorkoutTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

# ---------------------------
# Workouts
# ---------------------------

class WorkoutViewSet(viewsets.ModelViewSet):
    """
    GET list/detail uses ORM (read-only).
    POST uses stored procedure: CALL addWorkout(userID, workoutType, duration, workoutDate, RPE, notes)
    """
    serializer_class = WorkoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Restrict to current user
        return Workout.objects.filter(user_id=_uid(self.request)).select_related("workouttype").order_by("-workoutdate", "-workoutid")

    def create(self, request, *args, **kwargs):
        uid = _uid(request)
        data = request.data

        # API-level RPE validation to match DB CHECK (1..10)
        rpe = data.get("RPE", None)
        if rpe not in (None, ""):
            try:
                rpe_int = int(rpe)
                if not (1 <= rpe_int <= 10):
                    return Response({"error": "RPE must be an integer 1–10."}, status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                return Response({"error": "RPE must be an integer 1–10."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            rpe_int = None

        with connection.cursor() as cur:
            # Stored procedure insert
            cur.execute(
                "CALL addWorkout(%s, %s, %s, %s, %s, %s);",
                [
                    uid,
                    data.get("workoutType"),
                    data.get("duration"),      # HH:MM:SS
                    data.get("workoutDate"),   # YYYY-MM-DD
                    rpe_int,
                    data.get("notes"),
                ],
            )
            # Return the created row using LAST_INSERT_ID()
            cur.execute("SELECT LAST_INSERT_ID() AS id;")
            last_id = cur.fetchone()[0]
            cur.execute(
                """
                SELECT w.workoutID, w.userID, w.workoutType, wt.workoutName,
                       w.duration, w.workoutDate, w.RPE, w.notes
                FROM Workouts w
                JOIN WorkoutTypes wt ON w.workoutType = wt.workoutTypeID
                WHERE w.workoutID = %s AND w.userID = %s;
                """,
                [last_id, uid],
            )
            row = dictfetchall(cur)[0] if cur.rowcount else None

        if not row:
            # Fallback: list most recent if last_id not visible for any reason
            row = WorkoutSerializer(self.get_queryset().first()).data
            return Response(row, status=status.HTTP_201_CREATED)

        return Response(row, status=status.HTTP_201_CREATED)

# ---------------------------
# Scheduled Workouts
# ---------------------------

class ScheduledWorkoutViewSet(viewsets.ModelViewSet):
    """
    GET list/detail uses ORM (read-only).
    POST uses stored procedure: CALL addScheduledWorkout(userID, workoutType, scheduledDate, notes, duration)
    PATCH (status) validates against DB ENUM.
    """
    serializer_class = ScheduledWorkoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            ScheduledWorkout.objects
            .filter(user_id=_uid(self.request))
            .select_related("workouttype")
            .order_by("scheduleddate", "-scheduledworkoutid")
        )

    def create(self, request, *args, **kwargs):
        uid = _uid(request)
        data = request.data

        with connection.cursor() as cur:
            cur.execute(
                "CALL addScheduledWorkout(%s, %s, %s, %s, %s);",
                [
                    uid,
                    data.get("workoutType"),
                    data.get("scheduledDate"),  # YYYY-MM-DD
                    data.get("notes"),
                    data.get("duration"),       # HH:MM:SS or NULL
                ],
            )
            cur.execute("SELECT LAST_INSERT_ID() AS id;")
            last_id = cur.fetchone()[0]
            cur.execute(
                """
                SELECT scheduledWorkoutID, userID, workoutType, duration, scheduledDate, status
                FROM ScheduledWorkouts
                WHERE scheduledWorkoutID = %s AND userID = %s;
                """,
                [last_id, uid],
            )
            row = dictfetchall(cur)[0] if cur.rowcount else None

        if not row:
            row = ScheduledWorkoutSerializer(self.get_queryset().first()).data
            return Response(row, status=status.HTTP_201_CREATED)
        return Response(row, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["patch"], url_path="status")
    def update_status(self, request, pk=None):
        uid = _uid(request)
        new_status = (request.data.get("status") or "").lower()
        if new_status not in STATUS_CHOICES:
            return Response(
                {"error": f"status must be one of {sorted(list(STATUS_CHOICES))}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        with connection.cursor() as cur:
            # Ensure the row belongs to the user
            cur.execute(
                "UPDATE ScheduledWorkouts SET status = %s WHERE scheduledWorkoutID = %s AND userID = %s;",
                [new_status, pk, uid],
            )
            cur.execute(
                """
                SELECT scheduledWorkoutID, userID, workoutType, duration, scheduledDate, status
                FROM ScheduledWorkouts
                WHERE scheduledWorkoutID = %s AND userID = %s;
                """,
                [pk, uid],
            )
            row = dictfetchall(cur)
        if not row:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(row[0])
        # ENUM set validated per schema.

# ---------------------------
# Goals
# ---------------------------

class GoalViewSet(viewsets.ModelViewSet):
    """
    GET list/detail uses ORM (read-only).
    POST uses stored procedure: CALL addGoal(userID, goalType, notes, duration)
    Goal completion is handled by DB trigger on Workouts insert.
    """
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(user_id=_uid(self.request)).select_related("goaltype").order_by("-createdat", "-goalid")

    def create(self, request, *args, **kwargs):
        uid = _uid(request)
        data = request.data

        with connection.cursor() as cur:
            cur.execute(
                "CALL addGoal(%s, %s, %s, %s);",
                [uid, data.get("goalType"), data.get("notes"), data.get("duration")],
            )
            cur.execute("SELECT LAST_INSERT_ID() AS id;")
            last_id = cur.fetchone()[0]
            cur.execute(
                """
                SELECT g.goalID, g.userID, g.goalType, g.duration, g.notes, g.createdAt, g.completedAt, g.isComplete
                FROM Goals g
                WHERE g.goalID = %s AND g.userID = %s;
                """,
                [last_id, uid],
            )
            row = dictfetchall(cur)[0] if cur.rowcount else None

        if not row:
            row = GoalSerializer(self.get_queryset().first()).data
            return Response(row, status=status.HTTP_201_CREATED)
        return Response(row, status=status.HTTP_201_CREATED)
