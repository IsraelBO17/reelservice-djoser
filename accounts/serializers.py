from django.contrib.auth import get_user_model
from rest_framework import serializers
from djoser.serializers import (
    UserCreateSerializer as DjoserUserCreateSerializer,
    UserSerializer as DjoserUserSerializer,
    SendEmailResetSerializer,
)
from djoser.conf import settings


User = get_user_model()
    
class CustomUserSerializer(DjoserUserSerializer):
    groups = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
     )
    class Meta:
        model = User
        fields = ['id','groups','is_active']
        read_only_fields = ['is_active']

class CreateEmployeeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email',]

class PasswordResetSerializer(SendEmailResetSerializer):
    def get_user(self, is_active=True):
        try:
            user = User._default_manager.get(
                is_active=is_active,
                **{self.email_field: self.data.get(self.email_field, "")},
            )
            return user
        except User.DoesNotExist:
            pass
        if (
            settings.PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND
            or settings.USERNAME_RESET_SHOW_EMAIL_NOT_FOUND
        ):
            self.fail("email_not_found")

        