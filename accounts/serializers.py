from django.contrib.auth import get_user_model
from rest_framework import serializers
from djoser.serializers import (
    UserCreateSerializer as DjoserUserCreateSerializer,
    UserSerializer as DjoserUserSerializer,
)

User = get_user_model()

class CreateUserSerializer(DjoserUserCreateSerializer):
    groups = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
     )
    class Meta:
        model = User
        fields = ['id','email','password','groups','is_active']
        read_only_fields = ['is_active']
    
class UserSerializer(DjoserUserSerializer):
    groups = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
     )
    class Meta:
        model = User
        fields = ['id','email','groups','is_active']
        read_only_fields = ['groups','is_active']