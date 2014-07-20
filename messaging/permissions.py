from rest_framework import permissions

class AuthenticatedGetOrPostOnly(permissions.BasePermission):
    '''
    Custom permission to only allow user himself to read messages
    '''
        
    def has_permission(self, request, view):
            if (request.method == 'GET' and
                request.user.is_authenticated()):
                return True
            elif (request.method == 'POST'):
                return True
            return False    