# backend/serializer.py
from django.contrib.auth.models import User as AuthUser
from rest_framework import serializers

from .models import (
    WorkoutType,
    Workout,
    ScheduledWorkout,
    Goal,
)

# -----------------------------
# Auth User
# -----------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = ("id", "username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = AuthUser.objects.create_user(**validated_data)
        return user


# -----------------------------
# Profile (left as you had it)
# NOTE: If your Profile is a custom model (recommended),
#       we can switch this to Model=Profile once you confirm.
# -----------------------------
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:

        model = AuthUser
        fields = ("name", "sex", "height", "weight")
        read_only_fields = ["user"]

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})
        if full_name := user_data.get("get_full_name"):
            first, *last = full_name.split(" ")
            instance.first_name = first
            instance.last_name = " ".join(last) if last else ""
            instance.save()
        return super().update(instance, validated_data)


# -----------------------------
# Workout Types
# DB columns: workouttypeid, workoutname
# -----------------------------
class WorkoutTypeSerializer(serializers.ModelSerializer):
    # API-friendly aliases
    id = serializers.IntegerField(source="workouttypeid", read_only=True)
    name = serializers.CharField(source="workoutname", read_only=True)

    class Meta:
        model = WorkoutType
        # Expose both aliases and raw columns (raw are optional; remove if you prefer)
        fields = ("id", "name", "workouttypeid", "workoutname")
        read_only_fields = fields


# -----------------------------
# Workouts
# DB columns: workoutid, user(FK), workouttype(FK), duration, workoutdate, rpe, notes
# -----------------------------
class WorkoutSerializer(serializers.ModelSerializer):
    workout_id = serializers.IntegerField(source="workoutid", read_only=True)
    user_id = serializers.IntegerField(read_only=True)
    workout_type = serializers.IntegerField(source="workouttype_id", read_only=True)
    workout_type_name = serializers.CharField(source="workouttype.workoutname", read_only=True)
    workout_date = serializers.DateField(source="workoutdate", read_only=True)

    class Meta:
        model = Workout
        fields = (
            "workout_id",
            "user_id",
            "workout_type",
            "workout_type_name",
            "duration",
            "workout_date",
            "rpe",
            "notes",
            # raw (optional for debugging)
            "workoutid",
            "workouttype_id",
            "workoutdate",
        )
        read_only_fields = fields  # creates happen via stored procedures in the views


# -----------------------------
# Scheduled Workouts
# DB columns: scheduledworkoutid, user(FK), workouttype(FK), duration, scheduleddate, status
# -----------------------------
class ScheduledWorkoutSerializer(serializers.ModelSerializer):
    scheduled_workout_id = serializers.IntegerField(source="scheduledworkoutid", read_only=True)
    user_id = serializers.IntegerField(read_only=True)
    workout_type = serializers.IntegerField(source="workouttype_id", read_only=True)
    workout_type_name = serializers.CharField(source="workouttype.workoutname", read_only=True)
    scheduled_date = serializers.DateField(source="scheduleddate", read_only=True)

    class Meta:
        model = ScheduledWorkout
        fields = (
            "scheduled_workout_id",
            "user_id",
            "workout_type",
            "workout_type_name",
            "duration",
            "scheduled_date",
            "status",
            # raw (optional)
            "scheduledworkoutid",
            "scheduleddate",
            "workouttype_id",
        )
        read_only_fields = fields


# -----------------------------
# Goals
# DB columns: goalid, user(FK), goaltype(FK), duration, notes, createdat, completedat, iscomplete
# -----------------------------
class GoalSerializer(serializers.ModelSerializer):
    goal_id = serializers.IntegerField(source="goalid", read_only=True)
    user_id = serializers.IntegerField(read_only=True)
    goal_type = serializers.IntegerField(source="goaltype_id", read_only=True)
    goal_type_name = serializers.CharField(source="goaltype.workoutname", read_only=True)
    created_at = serializers.DateTimeField(source="createdat", read_only=True)
    completed_at = serializers.DateTimeField(source="completedat", read_only=True)
    is_complete = serializers.BooleanField(source="iscomplete", read_only=True)

    class Meta:
        model = Goal
        fields = (
            "goal_id",
            "user_id",
            "goal_type",
            "goal_type_name",
            "duration",
            "notes",
            "created_at",
            "completed_at",
            "is_complete",
            # raw (optional)
            "goalid",
            "goaltype_id",
            "createdat",
            "completedat",
            "iscomplete",
        )
        read_only_fields = fields
