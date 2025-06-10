#backend/serializer.py
from django.contrib.auth.models import User
from rest_framework import serializers

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