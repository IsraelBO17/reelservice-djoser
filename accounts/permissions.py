from rest_framework import permissions
# from rest_framework.permissions import SAFE_METHODS


class IsHRorAdmin(permissions.IsAuthenticated):
    '''Allows access to only admin users, and users who are in 'HR' group.'''
    def has_permission(self, request, view):
        super().has_permission(request, view)
        user = request.user
        return user.groups.filter(name='HR').exists() or user.is_staff

class IsEmployeeorAdmin(permissions.IsAuthenticated):
    '''Allows access to only admin users, and the user attached to the object.'''
    def has_object_permission(self, request, view):
        user = request.user
        return user.is_staff or user == obj.user