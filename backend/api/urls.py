from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    WorkoutTypeViewSet,
    WorkoutViewSet,
    ScheduledWorkoutViewSet,
    GoalViewSet,
    profile_detail,
)

router = DefaultRouter()
router.register(r'workout-types',    WorkoutTypeViewSet,       basename='workout-type')
router.register(r'workouts',         WorkoutViewSet,           basename='workout')
router.register(r'scheduled-workouts', ScheduledWorkoutViewSet, basename='scheduled-workout')
router.register(r'goals',            GoalViewSet,              basename='goal')

urlpatterns = [
    # GET /api/profile/  and PUT /api/profile/
    path('profile/', profile_detail, name='profile-detail'),

    # include all the router-registered endpoints
    path('', include(router.urls)),
]