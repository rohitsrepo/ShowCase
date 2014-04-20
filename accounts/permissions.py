from rest_framework import permissions


# This is where code becomes sexist.
class IsHimselfOrReadOnly(permissions.BasePermission):
    '''
    Custom permission to only allow user to edit it and rest to read.
    '''
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
    
        # Write permissions are only allowed to the user.
        return obj == request.user


class IsHimself(permissions.BasePermission):
    '''
    Custom permission to only allow user himself to edit.
    '''
        
    def has_object_permission(self, request, view, obj):
	# Permission is only allowed to the user.
	return obj == request.user
