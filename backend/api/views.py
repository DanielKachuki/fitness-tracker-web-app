from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializer import UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny


# Create your views here.
class CreateUserView(generics.CreateAPIView):
    #Look at all users, make sure no redundancy
    queryset = User.objects.all()
    #Tells view what data to accept to create user
    serializer_class = UserSerializer
    #Who can call this to create new user
    permission_classes = [AllowAny]


