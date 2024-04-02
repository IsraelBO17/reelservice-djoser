from django.contrib import admin
from .models import Employee, Job, Department, EmployeeType


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_number', 'employee_type', 'job', 'department')
    search_fields = ('employee_number', 'first_name', 'middle_name', 'last_name', 'job', 'department')
    ordering = ('user', 'department')

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'head')
    search_fields = ('name', 'head')
    ordering = ('name',)


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Job)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(EmployeeType)
