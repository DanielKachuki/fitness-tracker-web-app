#app/models.py
from django.db import models

class User(models.Model):
    SEX_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
    )
    userid = models.AutoField(db_column="userID", primary_key=True)
    username = models.CharField(db_column="userName", max_length=30)
    pw = models.CharField(db_column="PW", max_length=255)  # store hash only
    screenname = models.CharField(db_column="screenName", max_length=50)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, null=True, blank=True)
    height = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    class Meta:
        managed = False
        db_table = "Users"

    def __str__(self):
        return self.screenname or self.username


class WorkoutType(models.Model):
    workouttypeid = models.AutoField(db_column="workoutTypeID", primary_key=True)
    workoutname = models.CharField(db_column="workoutName", max_length=50, unique=True)

    class Meta:
        managed = False
        db_table = "WorkoutTypes"

    def __str__(self):
        return self.workoutname


class Workout(models.Model):
    workoutid = models.AutoField(db_column="workoutID", primary_key=True)
    user = models.ForeignKey(User, models.CASCADE, db_column="userID", related_name="workouts")
    workouttype = models.ForeignKey(
        WorkoutType, models.CASCADE, db_column="workoutType", related_name="workouts"
    )
    duration = models.TimeField()  # HH:MM:SS per MySQL TIME
    workoutdate = models.DateField(db_column="workoutDate")
    rpe = models.PositiveSmallIntegerField(db_column="RPE", null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = "Workouts"
        indexes = [
            models.Index(fields=["user", "workoutdate"], name="indexUserDate"),
        ]

    def __str__(self):
        return f"{self.user_id} • {self.workouttype_id} @ {self.workoutdate}"


class ScheduledWorkout(models.Model):
    STATUS_CHOICES = (
        ("scheduled", "Scheduled"),
        ("completed", "Completed"),
        ("missed", "Missed"),
        ("canceled", "Canceled"),
        ("rescheduled", "Rescheduled"),
    )
    scheduledworkoutid = models.AutoField(db_column="scheduledWorkoutID", primary_key=True)
    user = models.ForeignKey(User, models.CASCADE, db_column="userID", related_name="scheduled_workouts")
    workouttype = models.ForeignKey(
        WorkoutType, models.CASCADE, db_column="workoutType", related_name="scheduled_workouts"
    )
    duration = models.TimeField(null=True, blank=True)
    scheduleddate = models.DateField(db_column="scheduledDate")
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="scheduled")

    class Meta:
        managed = False
        db_table = "ScheduledWorkouts"
        indexes = [
            models.Index(fields=["user", "scheduleddate"], name="indexScheduledDate"),
        ]

    def __str__(self):
        return f"{self.scheduleddate} • {self.get_status_display()}"


class Goal(models.Model):
    goalid = models.AutoField(db_column="goalID", primary_key=True)
    user = models.ForeignKey(User, models.CASCADE, db_column="userID", related_name="goals")
    goaltype = models.ForeignKey(
        WorkoutType, models.CASCADE, db_column="goalType", related_name="goals", null=True, blank=True
    )
    duration = models.TimeField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    createdat = models.DateTimeField(db_column="createdAt")
    completedat = models.DateTimeField(db_column="completedAt", null=True, blank=True)
    iscomplete = models.BooleanField(db_column="isComplete", default=False)

    class Meta:
        managed = False
        db_table = "Goals"
        indexes = [
            models.Index(fields=["user", "goaltype", "iscomplete"], name="indexGoalStatus"),
        ]

    def __str__(self):
        return f"Goal #{self.goalid} ({'✔' if self.iscomplete else '…'})"
