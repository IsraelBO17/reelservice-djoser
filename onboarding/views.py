from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Employee, Job, Department, EmployeeType
from .serializers import EmployeeSerializer, CreateEmployeeSerializer, JobSerializer, DepartmentSerializer, EmployeeTypeSerializer, SendInviteSerializer
from .signals import send_invite_mail, deactivate_employee_user
from accounts.permissions import IsHRorAdmin, IsEmployeeorAdmin



class EmployeeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsHRorAdmin]
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = 'employee_number'

    def get_permissions(self):
        if self.action == 'employee':
            self.permission_classes = [IsEmployeeorAdmin]
        return super().get_permissions()


    def get_serializer_class(self):
        if self.action == 'create':
            return CreateEmployeeSerializer
        elif self.action == 'invite':
            return SendInviteSerializer
            
        return self.serializer_class

    def perform_destroy(self, instance, resignation_date):
        instance.deactivate_employee(resignation_date)
        deactivate_employee_user.send(sender=self.__class__, user=instance.user) 

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        resignation_date = serializer.validated_data.get('resignation_date')

        if instance.user == request.user:
            utils.logout_user(self.request)
        self.perform_destroy(instance, resignation_date)
        return Response(status=status.HTTP_204_NO_CONTENT)


    @action(detail=False, methods=["get"])
    def employee(self, request, *args, **kwargs):
        """Returns the employee record of the request user"""
        user = request.user
        try:
        	employee = Employee.objects.get(user=user)
        except Employee.DoesNotExist:
            return Response({"detail": "User has no employee attached with it"}, status=status.HTTP_404_NOT_FOUND)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)
    

    @action(detail=False, methods=["post"])
    def invite(self, request, *args, **kwargs):
        """Send an invitation email to the employee"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.get_user()

        if not user.is_active:
            response = send_invite_mail.send(sender=self.__class__, user=user, request=self.request)
            if response:
                return Response(data={'message':'Invitation successfully sent'}, status=status.HTTP_200_OK)
            else:
                return Response(data={'message':'Failed to send invitation'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={'message':'User is already active'}, status=status.HTTP_400_BAD_REQUEST)



class JobViewSet(viewsets.ModelViewSet):
    permission_classes = [IsHRorAdmin]
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    lookup_field = 'title'

    def perform_destroy(self, instance):
        instance.save(is_active=False)


class DepartmentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsHRorAdmin]
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    lookup_field = 'code'

    def perform_destroy(self, instance):
        instance.save(is_active=False)


class EmployeeTypeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsHRorAdmin]
    queryset = EmployeeType.objects.all()
    serializer_class = EmployeeTypeSerializer
    lookup_field = 'code'

    def perform_destroy(self, instance):
        instance.save(is_active=False)
