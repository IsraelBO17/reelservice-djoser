from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from datetime import date
from django.conf import settings
from django.core.validators import RegexValidator


User = get_user_model()

phone_regex = r'^\+?[1-9][0-9]{7,14}$' # r"(^\+?[\d{1,3}\s]?)\(?\d{3}\)?[-\s]\d{3}-\d{4}$"
phone_number_validator = RegexValidator(regex=phone_regex, message="Phone number must be in valid format (+xxxxxxxxxxxxxx).")

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

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Personal Details
    first_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=6)
    d_o_b = models.DateField(_("date of birth"))
    marital_status = models.CharField(choices=MARITAL_STATUS_CHOICES, max_length=8)
    religion = models.CharField(choices=RELIGION_CHOICES, max_length=9)
    nationality = models.CharField(max_length=150)
    profile_picture = models.ImageField(upload_to="profile_pictures/", null=True, blank=True)

    # Contact Details
    phone_number = models.CharField(max_length=20, unique=True, validators=[phone_number_validator])
    address = models.TextField(max_length=50)

    # Organisation Details
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

    @property
    def employee_number(self):
        "Returns the employee's number."
        return f'{settings.COMPANY_ABBR}-{self.employment_date.year}-{self.id:04d}'
    
    def get_short_name(self):
        "Return the short name for the user."
        return self.first_name

    def full_name(self):
        "Returns the employee's full name."
        return f'{self.first_name} {self.middle_name} {self.last_name}'
    
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
        return self.name


class EmployeeType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=2, unique=True)
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
        return self.name

