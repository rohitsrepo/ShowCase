from rest_framework import exceptions


def check_object_permissions(request, permissions, obj):
    '''
    Checks for object permissionsi for given obj from given set of permissions.
    '''
    for permission in permissions:
	if not permission().has_object_permission(request, None, obj=obj):
	    raise exceptions.PermissionDenied()


