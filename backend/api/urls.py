# api/urls.py  (APP urls)
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    WorkoutTypeViewSet, WorkoutViewSet, ScheduledWorkoutViewSet, GoalViewSet,
    profile_detail, CreateUserView
)

router = DefaultRouter()
router.register(r'workout-types', WorkoutTypeViewSet, basename='workout-types')
router.register(r'workouts', WorkoutViewSet, basename='workouts')
router.register(r'scheduled-workouts', ScheduledWorkoutViewSet, basename='scheduled-workouts')
router.register(r'goals', GoalViewSet, basename='goals')

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('register/', CreateUserView.as_view(), name='register'),
    path('profile/', profile_detail, name='profile-detail'),
    path('', include(router.urls)),
]
