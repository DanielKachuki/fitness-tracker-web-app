
from django.contrib.auth.models import User
from rest_framework import viewsets, generics, permissions
from .serializer import UserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import WorkoutType, Workout, ScheduledWorkout, Goal
from .serializer import (
    WorkoutTypeSerializer,
    WorkoutSerializer,
    ScheduledWorkoutSerializer,
    GoalSerializer,
    ProfileSerializer,
)

# Create your views here.
class CreateUserView(generics.CreateAPIView):
    #Look at all users, make sure no redundancy
    queryset = User.objects.all()
    #Tells view what data to accept to create user
    serializer_class = UserSerializer
    #Who can call this to create new user
    permission_classes = [AllowAny]

@api_view(['GET','PUT'])
@permission_classes([IsAuthenticated])
def profile_detail(request):
    profile = request.user.profile
    if request.method == 'GET':
        return Response(ProfileSerializer(profile).data)
    serializer = ProfileSerializer(profile, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

class WorkoutTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WorkoutType.objects.all()
    serializer_class = WorkoutTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

class WorkoutViewSet(viewsets.ModelViewSet):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    permission_classes = [permissions.IsAuthenticated]

class ScheduledWorkoutViewSet(viewsets.ModelViewSet):
    queryset = ScheduledWorkout.objects.all()
    serializer_class = ScheduledWorkoutSerializer
    permission_classes = [permissions.IsAuthenticated]

class GoalViewSet(viewsets.ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated]

