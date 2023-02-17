from dataclasses import field
from rest_framework import serializers
from .models import User as UserModel

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = [
            'name',
            'generation',
            'track',
            'is_admin'
        ]