from django.conf import settings
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from drf_spectacular.utils import extend_schema
from djoser.conf import settings as djoser_settings


class UserViewSet(DjoserUserViewSet):

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = djoser_settings.PERMISSIONS.user_create
        elif self.action == "activation":
            self.permission_classes = djoser_settings.PERMISSIONS.activation
        elif self.action == "resend_activation":
            # Changed the permission for resend activation to IsAdminUser
            self.permission_classes = djoser_settings.PERMISSIONS.resend_activation
        elif self.action == "list":
            self.permission_classes = djoser_settings.PERMISSIONS.user_list
        elif self.action == "reset_password":
            self.permission_classes = djoser_settings.PERMISSIONS.password_reset
        elif self.action == "reset_password_confirm":
            self.permission_classes = djoser_settings.PERMISSIONS.password_reset_confirm
        elif self.action == "set_password":
            self.permission_classes = djoser_settings.PERMISSIONS.set_password
        elif self.action == "set_username":
            self.permission_classes = djoser_settings.PERMISSIONS.set_username
        elif self.action == "reset_username":
            self.permission_classes = djoser_settings.PERMISSIONS.username_reset
        elif self.action == "reset_username_confirm":
            self.permission_classes = djoser_settings.PERMISSIONS.username_reset_confirm
        elif self.action == "destroy" or (
            self.action == "me" and self.request and self.request.method == "DELETE"
        ):
            self.permission_classes = djoser_settings.PERMISSIONS.user_delete

        return [permission() for permission in self.permission_classes]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance == request.user:
            utils.logout_user(self.request)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(["get"], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)

    def reset_username(self, request, *args, **kwargs):
        pass

    def reset_username_confirm(self, request, *args, **kwargs):
        pass



class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')

            response.set_cookie(
                'access',
                access_token,
                max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.SESSION_COOKIE_SECURE,
                httponly=settings.SESSION_COOKIE_HTTPONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
            response.set_cookie(
                'refresh',
                refresh_token,
                max_age=settings.AUTH_COOKIE_REFRESH_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.SESSION_COOKIE_SECURE,
                httponly=settings.SESSION_COOKIE_HTTPONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )

            # Remove refresh token from response
            del response.data['refresh']
            # Return response with only access token
            response.data = {'access': access_token}
        
        return response

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh')

        if refresh_token:
            request.data['refresh'] = refresh_token

        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data.get('access')

            response.set_cookie(
                'access',
                access_token,
                max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.SESSION_COOKIE_SECURE,
                httponly=settings.SESSION_COOKIE_HTTPONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )

        return response

class CustomTokenVerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        access_token = request.COOKIES.get('access')

        if access_token:
            request.data['token'] = access_token

        return super().post(request, *args, **kwargs)

@extend_schema(
    request=None,
    responses={204: None},
    methods=["POST"]
)
class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie('access')
        response.delete_cookie('refresh')

        return response