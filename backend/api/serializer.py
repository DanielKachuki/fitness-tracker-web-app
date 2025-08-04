#backend/serializer.py
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import (
    WorkoutType,
    Workout,
    ScheduledWorkout,
    Goal,
    Profile,
)

#convert serializers into JSON data
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        #Accept pass when creating user but do not return
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
            user = User.objects.create_user(**validated_data)
            return user

# Serializer for the user profile
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('name', 'sex', 'height', 'weight')
        read_only_fields = ['user']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        if full_name := user_data.get('get_full_name'):
            first, *last = full_name.split(' ')
            instance.user.first_name = first
            instance.user.last_name = " ".join(last) if last else ''
            instance.user.save()
        return super().update(instance, validated_data)

class WorkoutTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutType
        fields = ['id', 'name']

class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ['id', 'user', 'workout_type', 'duration', 'workout_date', 'rpe', 'notes']

class ScheduledWorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledWorkout
        fields = ['id', 'user', 'workout_type', 'duration', 'scheduled_date', 'notes']

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['id', 'user', 'goal_type', 'duration', 'notes', 'created_at', 'completed_at']