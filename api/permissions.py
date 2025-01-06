from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    '''
    Custom permission class to be used in views to restrict access
    to objects based on ownership.
    '''
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
