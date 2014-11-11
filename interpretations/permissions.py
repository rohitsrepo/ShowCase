from rest_framework import permissions


class IsInterpreterOrReadOnly(permissions.BasePermission):

    """
    Custom permission to allow only interpreter to edit/delete it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
