from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a superuser.'

    def handle(self, *args, **options):
        if not User.objects.filter(email='admin@email.com').exists():
            User.objects.create_superuser(
                email='admin@email.com',
                password='password'
            )
            print('Superuser has been created.')
        else:
            print('Superuser has already been created.')