from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Status

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = "__all__"