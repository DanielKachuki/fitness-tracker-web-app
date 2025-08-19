# backend/urls.py  (PROJECT urls)
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def root(_request):
    return JsonResponse({"ok": True, "message": "Backend is running", "api_base": "/api/"})

urlpatterns = [
    path('', root),                                # optional: simple root/health
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),  # DRF login for browsable API
    path('api/', include('api.urls')),             # ← include your APP urls here
]
