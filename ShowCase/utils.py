from rest_framework import exceptions


def check_object_permissions(request, permissions, obj):
    '''
    Checks for object permissionsi for given obj from given set of permissions.
    '''
    for permission in permissions:
	if not permission().has_object_permission(request, None, obj=obj):
	    raise exceptions.PermissionDenied()



from urllib import FancyURLopener
class BrowserSimulator(FancyURLopener):
     version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'
