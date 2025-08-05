from django.conf import settings
from django.db import models

class Profile(models.Model):
    user   = models.OneToOneField(
               settings.AUTH_USER_MODEL,
               on_delete=models.CASCADE,
               related_name='profile',
               db_column='user_id'
             )
    sex    = models.CharField(max_length=1, choices=[('M','Male'),('F','Female'),('O','Other')], default='O')
    height = models.FloatField(null=True, blank=True, help_text='cm')
    weight = models.FloatField(null=True, blank=True, help_text='kg')

    class Meta:
        db_table = 'api_profile'
        managed = False   # keep using the existing SQL table

    def __str__(self):
        return f"{self.user.username}'s profile"

class WorkoutType(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=50, unique=True, db_column="workoutName")

    class Meta:
        db_table = "workouttypes"
        managed = False  # since using the existing SQL schema

    def __str__(self):
        return self.name


class Goal(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="goals",
        db_column="userID"
    )
    goal_type = models.ForeignKey(
        WorkoutType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="goals",
        db_column="goalType"
    )
    duration = models.DurationField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_column="createdAt")
    completed_at = models.DateTimeField(null=True, blank=True, db_column="completedAt")

    class Meta:
        db_table = "goals"
        managed = False

    def __str__(self):
        label = self.goal_type.name if self.goal_type else "—"
        return f"{self.user.username}’s goal: {label}"


class Workout(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="workouts",
        db_column="userID"
    )
    workout_type = models.ForeignKey(
        WorkoutType,
        on_delete=models.CASCADE,
        related_name="workouts",
        db_column="workoutType"
    )
    duration = models.DurationField()
    workout_date = models.DateField(db_column="workoutDate")
    rpe = models.PositiveSmallIntegerField(null=True, blank=True, db_column="RPE")
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "workouts"
        managed = False

    def __str__(self):
        return f"{self.user.username} — {self.workout_type.name} on {self.workout_date}"


class ScheduledWorkout(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="scheduled_workouts",
        db_column="userID"
    )
    workout_type = models.ForeignKey(
        WorkoutType,
        on_delete=models.CASCADE,
        related_name="scheduled_workouts",
        db_column="workoutType"
    )
    duration = models.DurationField(null=True, blank=True)
    scheduled_date = models.DateField(db_column="scheduledDate")
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "scheduledworkouts"
        managed = False

    def __str__(self):
        return f"Scheduled {self.workout_type.name} for {self.user.username} on {self.scheduled_date}"
