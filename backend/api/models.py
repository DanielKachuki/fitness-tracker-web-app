from django.db import models

class User(models.Model):
    user_id     = models.AutoField(primary_key=True, db_column='userID')
    username    = models.CharField(max_length=30, unique=True, db_column='userName')
    password    = models.CharField(max_length=255,       db_column='PW')
    screen_name = models.CharField(max_length=50,        db_column='screenName')
    sex         = models.CharField(
                    max_length=1,
                    choices=[('M','Male'),('F','Female')],
                    blank=True,
                    null=True,
                    db_column='sex'
                  )
    height      = models.DecimalField(
                    max_digits=6,
                    decimal_places=2,
                    blank=True,
                    null=True,
                    db_column='height'
                  )
    weight      = models.DecimalField(
                    max_digits=6,
                    decimal_places=2,
                    blank=True,
                    null=True,
                    db_column='weight'
                  )

    class Meta:
        db_table = 'Users'

    def __str__(self):
        return self.screen_name


class WorkoutType(models.Model):
    workout_type_id = models.AutoField(primary_key=True, db_column='workoutTypeID')
    workout_name    = models.CharField(max_length=50, unique=True, db_column='workoutName')

    class Meta:
        db_table = 'WorkoutTypes'

    def __str__(self):
        return self.workout_name


class Workout(models.Model):
    workout_id   = models.AutoField(primary_key=True, db_column='workoutID')
    user         = models.ForeignKey(
                     User,
                     on_delete=models.CASCADE,
                     related_name='workouts',
                     db_column='userID'
                   )
    workout_type = models.ForeignKey(
                     WorkoutType,
                     on_delete=models.CASCADE,
                     related_name='workouts',
                     db_column='workoutType'
                   )
    duration     = models.DurationField(db_column='duration')
    workout_date = models.DateField(db_column='workoutDate')
    rpe          = models.PositiveSmallIntegerField(
                     blank=True,
                     null=True,
                     db_column='RPE'
                   )
    notes        = models.TextField(blank=True, null=True, db_column='notes')

    class Meta:
        db_table = 'Workouts'
        indexes = [
            models.Index(fields=['user'], name='indexUserDate'),
        ]

    def __str__(self):
        return f"{self.user.screen_name} – {self.workout_type.workout_name} on {self.workout_date}"


class ScheduledWorkout(models.Model):
    scheduled_workout_id = models.AutoField(primary_key=True, db_column='scheduledWorkoutID')
    user                 = models.ForeignKey(
                             User,
                             on_delete=models.CASCADE,
                             related_name='scheduled_workouts',
                             db_column='userID'
                           )
    workout_type         = models.ForeignKey(
                             WorkoutType,
                             on_delete=models.CASCADE,
                             related_name='scheduled_workouts',
                             db_column='workoutType'
                           )
    duration             = models.DurationField(
                             blank=True,
                             null=True,
                             db_column='duration'
                           )
    scheduled_date       = models.DateField(db_column='scheduledDate')

    class Meta:
        db_table = 'ScheduledWorkouts'
        indexes = [
            models.Index(fields=['user', 'scheduled_date'], name='indexScheduledDate'),
        ]

    def __str__(self):
        return f"{self.user.screen_name} scheduled {self.workout_type.workout_name} for {self.scheduled_date}"


class Goal(models.Model):
    goal_id       = models.AutoField(primary_key=True, db_column='goalID')
    user          = models.ForeignKey(
                      User,
                      on_delete=models.CASCADE,
                      related_name='goals',
                      db_column='userID'
                    )
    goal_type     = models.ForeignKey(
                      WorkoutType,
                      on_delete=models.CASCADE,
                      related_name='goals',
                      blank=True,
                      null=True,
                      db_column='goalType'
                    )
    duration      = models.DurationField(
                      blank=True,
                      null=True,
                      db_column='duration'
                    )
    notes         = models.TextField(blank=True, null=True, db_column='notes')
    created_at    = models.DateTimeField(
                      auto_now_add=True,
                      db_column='createdAt'
                    )
    completed_at  = models.DateTimeField(
                      blank=True,
                      null=True,
                      db_column='completedAt'
                    )
    is_complete   = models.BooleanField(
                      default=False,
                      db_column='isComplete'
                    )

    class Meta:
        db_table = 'Goals'
        indexes = [
            models.Index(fields=['user', 'goal_type', 'is_complete'], name='indexGoalStatus'),
        ]

    def __str__(self):
        status = "✔️" if self.is_complete else "❌"
        return f"{self.user.screen_name}'s goal {status}"
