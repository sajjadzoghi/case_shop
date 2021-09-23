from rest_framework import permissions


class NotAuthenticated(permissions.BasePermission):
    # permission to allow only unregistered users to register
    def has_permission(self, request, view):
        return not request.user
