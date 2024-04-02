# from django.urls import path
from rest_framework import routers
from .views import EmployeeViewSet, JobViewSet, DepartmentViewSet, EmployeeTypeViewSet


router = routers.SimpleRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'jobs', JobViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'employee_types', EmployeeTypeViewSet)

urlpatterns = router.urls