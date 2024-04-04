from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
import logging


class Command(BaseCommand):
    help = 'Creates Employee, and HR groups'

    def handle(self, *args, **options):
        try:
            hr_group,_ = Group.objects.get_or_create(name='HR')
            employee_group,_ = Group.objects.get_or_create(name='Employee')

            hr_group.permissions.add(
                Permission.objects.get(codename='add_employee'),
                Permission.objects.get(codename='change_employee'),
                Permission.objects.get(codename='add_job'),
                Permission.objects.get(codename='change_job'),
                Permission.objects.get(codename='view_job'),
                Permission.objects.get(codename='add_department'),
                Permission.objects.get(codename='change_department'),
                Permission.objects.get(codename='view_department'),
                Permission.objects.get(codename='add_employeetype'),
                Permission.objects.get(codename='change_employeetype'),
                Permission.objects.get(codename='view_employeetype'),
            )
            employee_group.permissions.add(
                Permission.objects.get(codename='change_user'),
                Permission.objects.get(codename='view_employee'),
            )
            self.stdout.write(self.style.SUCCESS('Employee, and HR groups created successfully.'))
        except Exception as ex:
            logging.exception(f'An exception occurred: {ex}')
