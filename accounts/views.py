from .models import User
from .serializers import NewUserSerializer, ExistingUserSerializer, PasswordUserSerializer, BookmarkSerializer, FollowSerializer
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics, permissions
from .permissions import IsHimselfOrReadOnly, IsHimself
from django.contrib.auth import authenticate, login, logout
from ShowCase.utils import check_object_permissions
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from compositions.models import Composition
from django.db.models import Q


class UserList(APIView):

    '''
    Creates and lists users.
    '''
    # TODO Change this permission to AllowANY-Catptcha or token authentication
    # required.
    permission_classes = (permissions.AllowAny,)

    def is_registered(self, email):
        if (User.objects.filter(email=email).exists()):
            print "already there"
            return True
        print "not here yet"
        return False

    def register_user(self, ser):
        if ser.is_valid():
            print "user is valid"
            ser.save()
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


    def post(self, request, format=None):
        if self.is_registered(request.DATA.get('email', '')):
            return Response(status=status.HTTP_200_OK)

        login_type = request.DATA['login_type']

        if login_type == "NT":
            print "the native way"
        elif (login_type == "FB" or login_type == "TW"):
            print 'the social way'
            request.DATA['password'] = '!@#$%^&$@$%'
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        print request.DATA

        ser = NewUserSerializer(data=request.DATA, context={'request': request})
        return self.register_user(ser)


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
        ser = ExistingUserSerializer(
            user, data=request.DATA, partial=True, context={'request': request})
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

    check_object_permissions(
        request, reset_password.cls.permission_classes, user)

    serializer = PasswordUserSerializer(
        data=request.DATA, context={'user': user})
    if serializer.is_valid():
        user.set_password(serializer.object['new_password'])
        user.save()
        return Response()
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_user(request, format=None):
    email = request.DATA.get('email')
    password = request.DATA.get('password')
    login_type= request.DATA.get('login_type')
    try:
        if login_type == "NT":
            user = authenticate(username=email, password=password)
        elif login_type == "FB" or login_type == "TW":
            user = authenticate(username=email, password='!@#$%^&$@$%')

        if user.is_active:
            login(request, user)
            return Response(ExistingUserSerializer(user, context={'request': request}).data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_402_PAYMENT_REQUIRED)
    except Exception:
        if not User.objects.filter(email=email).exists():
            return Response(status=status.HTTP_409_CONFLICT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def logout_user(request, format=None):
    logout(request)
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def get_current_user(request, format=None):
    if request.user.is_authenticated():
        return Response(ExistingUserSerializer(request.user, context={'request': request}).data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def search_artist(request, format=None):
    if not request.user.is_authenticated():
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    query = request.GET.get('q', '')
    artists = User.objects.filter(
        Q(pk=request.user.id) | Q(is_artist=True),
        Q(name__icontains=query)
    )[:20]

    ser = ExistingUserSerializer(artists, context={'request': request})

    return Response(ser.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes((permissions.IsAuthenticated, IsHimself))
def user_bookmarks(request, pk, format=None):
    check_object_permissions(
        request, user_bookmarks.cls.permission_classes, User.objects.get(pk=pk))
    if request.method == 'GET':
        serializer = BookmarkSerializer(
            request.user, context={request: request})
        return Response(serializer.data)
    elif request.method == 'POST':
        bookmarks = request.DATA.get('bookmarks')
        if not bookmarks:
            return Response({"bookmarks": "This field is required"}, status=status.HTTP_400_BAD_REQUEST)
        request.user.bookmarks.add(*bookmarks)
        return Response(status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        bookmarks = request.DATA.get('bookmarks')
        if not bookmarks:
            return Response({"bookmarks": "This field is required"}, status=status.HTTP_400_BAD_REQUEST)

        request.user.bookmarks.remove(*bookmarks)
        serializer = BookmarkSerializer(request.user)
        return Response(serializer.data)


@api_view(['GET', 'PUT', 'POST'])
@permission_classes((permissions.IsAuthenticated, IsHimself))
def user_follows(request, pk, format=None):
    check_object_permissions(
        request, user_follows.cls.permission_classes, User.objects.get(pk=pk))
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
