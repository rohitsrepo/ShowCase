from rest_framework import permissions


class HasNotVotedBeforeOrReadOnly(permissions.BasePermission):
    """
    Custom permission to not allow user who has already voted.
    """

    def has_object_permission(self, request, view, obj):
	if request.method in permissions.SAFE_METHODS:
	    return True

	if obj.has_voted(request.user):
	    return False
	return True
