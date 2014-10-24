from rest_framework import permissions


class AuthenticatedGetOrPostOnly(permissions.BasePermission):

    '''
    Custom permission to only allow user himself to read messages
    '''

    def has_permission(self, request, view):
        if (request.method == 'GET'):
            return str(request.user.id) == view.kwargs['pk']
        elif (request.method == 'POST'):
            return True
