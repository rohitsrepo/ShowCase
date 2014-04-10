from .models import User
from .serializers import NewUserSerializer, ExistingUserSerializer, PasswordUserSerializer
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status, exceptions
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics, permissions
from .permissions import IsHimselfOrReadOnly, IsHimself

def check_object_permissions(request, permissions, obj):
    '''
    Checks for object permissionsi for given obj from given set of permissions.
    '''
    for permission in permissions:
	if not permission().has_object_permission(request,None,obj=obj):
	    raise exceptions.PermissionDenied()

class UserList(generics.ListCreateAPIView):
    '''
    Creates and lists users.
    '''
    queryset = User.objects.all()
    serializer_class = NewUserSerializer
    #TODO Change this permission to AllowANY-Catptcha or token authentication required.
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    '''
    Retrieves, updates and deletes a particular user.
    '''
    queryset = User.objects.all()
    serializer_class = ExistingUserSerializer
    permission_classes = (IsHimselfOrReadOnly,)

@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated, IsHimself))
def reset_password(request, pk, format=None):
    '''
    Changes user password.

    Offloading validation like both values entered in new password fields are same, to frontend.
    '''
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        raise Http404
    
    check_object_permissions(request, reset_password.cls.permission_classes, user) 
    
    serializer = PasswordUserSerializer(data=request.DATA,context={'user':user})
    if serializer.is_valid():
	user.set_password(serializer.object['new_password'])
	user.save()
	return Response()
    else:
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

