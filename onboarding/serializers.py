from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import serializers
from .models import Employee, Job, Department, EmployeeType
from .signals import send_invite_mail
from accounts.serializers import CustomUserSerializer, CreateEmployeeUserSerializer


User = get_user_model()

class EmployeeSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    job = serializers.SlugRelatedField(queryset=Job.objects.all(), slug_field="title")
    department = serializers.SlugRelatedField(queryset=Department.objects.all(), slug_field="code")
    employee_type = serializers.SlugRelatedField(queryset=EmployeeType.objects.all(), slug_field="code")
    
    class Meta:
        model = Employee
        fields = '__all__'
        read_only_fields = ['resignation_date','is_leave','is_active','created_at','updated_at']
    


class CreateEmployeeSerializer(EmployeeSerializer):
    user = CreateEmployeeUserSerializer(required=True)
    send_invite = serializers.BooleanField(default=True, write_only=True)

    class Meta:
        model = Employee
        fields = '__all__'
        read_only_fields = ['resignation_date','is_leave','is_active','created_at','updated_at']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        send_invite = validated_data.pop('send_invite')
        request = self.context.get('request')

        try:
            user = User.objects.create_employee_user(**user_data)
            employee = Employee.objects.create(user=user, **validated_data)
        except Exception as exc:
            return exc

        if send_invite:
            send_invite_mail.send(
                sender=self.__class__, user=user, request=request,
            )
        return employee


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ['is_active']


class DepartmentSerializer(serializers.ModelSerializer):
    head = serializers.SlugRelatedField(queryset=Employee.objects.all(), slug_field="employee_number")
    class Meta:
        model = Department
        fields = '__all__'
        read_only_fields = ['is_active']


class EmployeeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeType
        fields = '__all__'
        read_only_fields = ['is_active']


class SendInviteSerializer(serializers.Serializer):
    default_error_messages = {
        "email_not_found": 'User with given email does not exists.'
    }
    email = serializers.EmailField()

    def get_user(self):
        try:
            user = User._default_manager.get(
                email=self.data.get('email', ''),
            )
            if user:
                return user
        except User.DoesNotExist:
            pass
        
        self.fail("email_not_found")