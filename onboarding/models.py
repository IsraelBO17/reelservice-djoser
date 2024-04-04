from django.db import models
from django.db.models import F, Func, Value
from django.db.models.functions import Concat, ExtractYear, LPad, Cast
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from datetime import date
from django.conf import settings
from django.core.validators import RegexValidator
from django_countries.fields import CountryField


class ConcatOp(models.Func):
    arg_joiner = " || "
    function = None
    output_field = models.CharField()
    template = "%(expressions)s"

User = get_user_model()

phone_regex = r'^\+?[1-9][0-9]{7,14}$'
phone_number_validator = RegexValidator(regex=phone_regex, message="Phone number must be in valid format (+xxxxxxxxxxxxxx).")

class CapitalizeCharField(models.CharField):
    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        return value.capitalize() if value is not None else value

class Employee(models.Model):
    # Choices for gender field
    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
    )

    # Choices for marital_status field
    MARITAL_STATUS_CHOICES = (
        ("Single", "Single"),
        ("Married", "Married"),
        ("Divorced", "Divorced"),
        ("Widow", "Widow"),
        ("Widower", "Widower"),
    )

    # Choices for religion field
    RELIGION_CHOICES = (
        ("Christian", "Christian"),
        ("Muslim", "Muslim"),
        ("Atheist", "Atheist"),
        ("Others", "Others"),
    )

    # Company Abbrreviation
    COMPANY_ABBR = 'RBS'

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Personal Details
    first_name = CapitalizeCharField(max_length=150)
    middle_name = CapitalizeCharField(max_length=150)
    last_name = CapitalizeCharField(max_length=150)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=6)
    d_o_b = models.DateField(_("date of birth"))
    marital_status = models.CharField(choices=MARITAL_STATUS_CHOICES, max_length=8)
    religion = models.CharField(choices=RELIGION_CHOICES, max_length=9)
    nationality = CountryField()
    profile_picture = models.ImageField(upload_to="profile_pictures/", null=True, blank=True)

    # Contact Details
    phone_number = models.CharField(max_length=20, unique=True, validators=[phone_number_validator])
    address = models.TextField(max_length=150)

    # Organisation Details
    employee_number = models.GeneratedField(
        # Employeenumber format: 'RBS-YYYY-0000'
        expression=ConcatOp(
            Value('RBS'),
            Value('-'),
            Cast(ExtractYear('employment_date'), output_field=models.CharField()),
            Value('-'),
            LPad(Cast('id', output_field=models.CharField()), 4, Value('0'))
        ),
        output_field=models.CharField(max_length=15),
        db_persist=True,
        unique=True
    )
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    employee_type = models.ForeignKey('EmployeeType', on_delete=models.CASCADE)
    employment_date = models.DateField(_("date of employment"), default=date.today)
    resignation_date = models.DateField(_("date of resignation"), null=True, blank=True)
    is_leave = models.BooleanField(
        _("on leave"),
        default=False,
        help_text=_(
            "Designates whether this employee is/isn't on leave."
            "Select this if employee is on leave."
        ),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this employee is still employed."
            "Unselect this instead of deleting employee record."
        ),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # @property
    # def employee_number(self):
    #     "Returns the employee's number."
    #     return f'{self.COMPANY_ABBR}-{self.employment_date.year}-{self.id:04d}'
    
    def get_short_name(self):
        "Returns the short name for the employee."
        return self.first_name

    def full_name(self):
        "Returns the employee's full name."
        return f'{self.first_name} {self.middle_name} {self.last_name}'

    def deactivate_employee(self, resignation_date=date.today()):
        """Deactivates an employee."""
        self.resignation_date = resignation_date
        self.is_active = False
        self.user.is_active = False
        self.save()
        return self.is_active
    
    def __str__(self):
        return self.employee_number


class Job(models.Model):
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, max_length=200)
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this job should be treated as active. "
            "Unselect this instead of deleting jobs."
        ),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Department(models.Model):
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=5, unique=True)
    description = models.TextField(blank=True, max_length=200)
    head = models.OneToOneField(Employee, on_delete=models.CASCADE, null=True, blank=True, related_name='department_head')
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this department should be treated as active. "
            "Unselect this instead of deleting departments."
        ),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code


class EmployeeType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=5, unique=True)
    description = models.TextField(blank=True, max_length=200)
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this employee type should be treated as active. "
            "Unselect this instead of deleting employee types."
        ),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code

