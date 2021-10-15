from rest_framework import permissions


class IsOwnerOfAddress(permissions.BasePermission):
    # permission to ensure that information of each customer can 'view', 'change' or 'delete' only by its owner
    def has_object_permission(self, request, view, obj):
        return obj.customer == request.user


class IsOwnerOfPassword(permissions.BasePermission):
    # permission to ensure that information of each customer can 'view', 'change' or 'delete' only by its owner
    def has_object_permission(self, request, view, obj):
        return obj.password == request.user.password


class IsOwnerOfMobile(permissions.BasePermission):
    # permission to ensure that information of each customer can 'view', 'change' or 'delete' only by its owner
    def has_object_permission(self, request, view, obj):
        return obj.mobile == request.user.mobile
