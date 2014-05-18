from .models import User
from .serializers import NewUserSerializer, ExistingUserSerializer, PasswordUserSerializer
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status, exceptions
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics, permissions
from .permissions import IsHimselfOrReadOnly, IsHimself
from django.contrib.auth import authenticate, login, logout


def check_object_permissions(request, permissions, obj):
    '''
    Checks for object permissionsi for given obj from given set of permissions.
    '''
    for permission in permissions:
	if not permission().has_object_permission(request, None, obj=obj):
	    raise exceptions.PermissionDenied()


class UserList(generics.ListCreateAPIView):
    '''
    Creates and lists users.
    '''
    queryset = User.objects.all()
    serializer_class = NewUserSerializer
    # TODO Change this permission to AllowANY-Catptcha or token authentication required.
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
    
    serializer = PasswordUserSerializer(data=request.DATA, context={'user': user})
    if serializer.is_valid():
	user.set_password(serializer.object['new_password'])
	user.save()
	return Response()
    else:
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def login_user(request, format=None):
	# email = request.DATA.get('email')
	# password = make_password(request.DATA.get('password'))
	# user = authenticate(username=email, password=password)

	# if user is not None:
	if request.user.is_active:
	    login(request, request.user)
	    print request.user
	else:
	    print "Account has been disabled"

	# else:
	#    print "user name and password do not sound correct."


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def logout_user(request, format=None):
    logout(request)
    print "user has been logged out, we guess!!!"


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def get_current_user(request, format=None):
    if request.user.is_authenticated():
	return Response(ExistingUserSerializer(request.user, context={'request': request}).data, status=status.HTTP_200_OK)
    else:
	return Response(status=status.HTTP_401_UNAUTHORIZED)
