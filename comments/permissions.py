from rest_framework import permissions


class IsCommenterOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only commenter to edit/delete it.
    """

    def has_object_permission(self, request, view, obj):
	if request.method in permissions.SAFE_METHODS:
	    return True
	return obj.commenter == request.user
