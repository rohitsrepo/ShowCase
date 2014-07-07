from .models import User
from .serializers import NewUserSerializer, ExistingUserSerializer, PasswordUserSerializer, BookmarkSerializer, FollowSerializer
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics, permissions
from .permissions import IsHimselfOrReadOnly, IsHimself
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from ShowCase.utils import check_object_permissions
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView


class UserList(generics.ListCreateAPIView):
    '''
    Creates and lists users.
    '''
    queryset = User.objects.all()
    serializer_class = NewUserSerializer
    # TODO Change this permission to AllowANY-Catptcha or token authentication required.
    permission_classes = (permissions.AllowAny,)


class UserDetailOld(generics.RetrieveUpdateDestroyAPIView):
    '''
    Retrieves, updates and deletes a particular user.
    '''
    queryset = User.objects.all()
    serializer_class = ExistingUserSerializer
    permission_classes = (IsHimselfOrReadOnly,)

class UserDetail(APIView):
    '''
    Retrieves, updates and deletes a particular user.
    '''

    permission_classes = ((IsHimselfOrReadOnly,))

    def get_user(self, pk, request):
	user = get_object_or_404(User, pk=pk)
	check_object_permissions(request, self.permission_classes, user)
	return user

    def get(self, request, pk, format=None):
	user = self.get_user(pk, request)
	ser = ExistingUserSerializer(user, context={'request': request})
	ser.data['IsFollowed'] = False

	if request.user.is_authenticated() and request.user.follows.filter(pk=pk).exists():
	    ser.data['IsFollowed'] = True
	return Response(ser.data)

    def put(self, request, pk, format=None):
	user = self.get_user(pk, request)
	ser = ExistingUserSerializer(user, data=request.DATA, partial=True, context={'request': request})
	if ser.is_valid():
	    ser.save()
	    return Response(ser.data)
	return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
	user = self.get_user(pk, request)
	user.delete()
	return Response(status=status.HTTP_204_NO_CONTENT)


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
#@permission_classes((permissions.IsAuthenticated,))
def login_user(request, format=None):
	email = request.DATA.get('email')
	print email
	password = request.DATA.get('password')
	print password
	try:
		user = authenticate(username=email, password=password)
	
		# if user is not None:
		if user.is_active:
		    login(request, user)
		    return Response(ExistingUserSerializer(user, context={'request': request}).data, status=status.HTTP_200_OK)
		else:
		    return Response(status=status.HTTP_403_FORBIDDEN)
	except Exception as ex:
	    print ex
	    return Response(status=status.HTTP_401_UNAUTHORIZED)

	# else:
	#    print "user name and password do not sound correct."


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def logout_user(request, format=None):
    logout(request)
    return Response(status=status.HTTP_200_OK);


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def get_current_user(request, format=None):
    if request.user.is_authenticated():
	return Response(ExistingUserSerializer(request.user, context={'request': request}).data, status=status.HTTP_200_OK)
    else:
	return Response(status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET', 'PUT', 'POST'])
@permission_classes((permissions.IsAuthenticated, IsHimself))
def user_bookmarks(request, pk, format=None):
    check_object_permissions(request, user_bookmarks.cls.permission_classes, User.objects.get(pk=pk))
    if request.method == 'GET':
	serializer = BookmarkSerializer(request.user, context={request: request}) 
	return Response(serializer.data)
    elif request.method == 'PUT':
	bookmarks = request.DATA.get('bookmarks')
	request.user.bookmarks.add(*bookmarks)
	serializer = BookmarkSerializer(request.user)
	return Response(serializer.data)
    elif request.method == 'POST':
	bookmarks = request.DATA['bookmarks']
	request.user.bookmarks.remove(*bookmarks)
	serializer = BookmarkSerializer(request.user)
	return Response(serializer.data)

@api_view(['GET', 'PUT', 'POST'])
@permission_classes((permissions.IsAuthenticated, IsHimself))
def user_follows(request, pk, format=None):
    check_object_permissions(request, user_follows.cls.permission_classes, User.objects.get(pk=pk))
    if request.method == 'GET':
	serializer = FollowSerializer(request.user, context={request: request}) 
	return Response(serializer.data)
    elif request.method == 'PUT':
	follows = request.DATA.get('follows')
	request.user.follows.add(*follows)
	serializer = FollowSerializer(request.user)
	return Response(serializer.data)
    elif request.method == 'POST':
	follows = request.DATA['follows']
	request.user.follows.remove(*follows)
	serializer = FollowSerializer(request.user)
	return Response(serializer.data)
