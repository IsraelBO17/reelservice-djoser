from drf_spectacular.extensions import OpenApiAuthenticationExtension
from django.conf import settings


class MyAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = 'accounts.authentication.CustomJWTAuthentication'
    name = 'cookieAuth'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'apiKey',
            'in': 'header',
            'name': settings.AUTH_COOKIE,
        }

        