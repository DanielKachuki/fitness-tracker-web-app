from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views import CreateUserView, profile_detail



urlpatterns = [
    path('admin/', admin.site.urls),

    # auth & registration
    path("api/user/register/", CreateUserView.as_view(), name="register"),
    path("api/token/", TokenObtainPairView.as_view(), name="get_token"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("api-auth/", include("rest_framework.urls")),

    path('api/profile/',        profile_detail,                  name='profile-detail'),

    # all other API routes (workouts, goals, profile, etc.)
    path("api/", include("api.urls")),
]
