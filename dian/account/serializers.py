from rest_framework import serializers
from .models import User
from .models import SeedUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'alias')

class SeedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeedUser
        fields = ('name', 'address', 'title', 'phone')
