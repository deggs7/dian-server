from rest_framework import serializers
from account.models import User
from account.models import SeedUser
from account.models import Member


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'alias')


class SeedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeedUser
        fields = ('name', 'address', 'title', 'phone')


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
