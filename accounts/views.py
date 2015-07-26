from .models import User
from .serializers import NewUserSerializer, ExistingUserSerializer, PasswordUserSerializer, FollowSerializer
from .artistSerializers import PaginatedUserCompositionSerializer, PaginatedUserInterpretationSerializer
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
from compositions.serializers import CompositionSerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.core.exceptions import ValidationError


class UserList(APIView):

    '''
    Creates and lists users.
    '''
    # TODO Change this permission to AllowANY-Catptcha or token authentication
    # required.
    permission_classes = (permissions.AllowAny,)

    def login_user(self, request, user):
        if user.is_active:
            user = authenticate(username=request.DATA['email'], password=request.DATA['password'])
            if (user is None):
                return Response(status=status.HTTP_409_CONFLICT)
            login(request, user)
            ser = ExistingUserSerializer(user, context={'request': request})
            return Response(data=ser.data)
        return Response(status=status.HTTP_402_PAYMENT_REQUIRED)

    def post(self, request, format=None):
        user_mail = request.DATA.get('email', '')
        if (user_mail):
            try:
                user = User.objects.get(email=user_mail)
                return self.login_user(request, user)
            except User.DoesNotExist:
                ser = NewUserSerializer(data=request.DATA, context={'request': request})
                if ser.is_valid():
                    ser.object.login_type = User.NATIVE
                    user = ser.save()
                    return self.login_user(request, user)
                else:
                    return Response(data=ser.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
                return Response(data={'email': 'This field is required'}, status=status.HTTP_400_BAD_REQUEST)


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
        return Response(data=ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_user(pk, request)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserBookmarksAdd(APIView):

    '''
    Retrieves, updates and deletes a particular user.
    '''

    permission_classes = ((permissions.IsAuthenticatedOrReadOnly,))

    def post(self, request, format=None):
        bookmarks = request.DATA.get('bookmarks')
        if not bookmarks:
            return Response({"bookmarks": "This field is required"}, status=status.HTTP_400_BAD_REQUEST)
        request.user.bookmarks.add(*bookmarks)
        return Response(status=status.HTTP_201_CREATED)

class UserBookmarksDelete(APIView):

    '''
    Retrieves, updates and deletes a particular user.
    '''

    permission_classes = ((permissions.IsAuthenticatedOrReadOnly,))

    def delete(self, request, pk, format=None):
        request.user.bookmarks.remove(pk)
        return Response(status=status.HTTP_201_CREATED)

class UserBookmarksRead(APIView):

    '''
    Retrieves, updates and deletes a particular user.
    '''

    permission_classes = ((permissions.AllowAny,))

    def get(self, request, pk, format=None):
        user = get_object_or_404(User, pk=pk)
        user_collection = user.bookmarks.all().order_by('-id')

        page_num = request.GET.get('page', 1)
        paginator = Paginator(user_collection, 9)

        try:
            this_page_compositions = paginator.page(page_num)
        except PageNotAnInteger:
            this_page_compositions = paginator.page(1)
        except EmptyPage:
            raise Http404

        serializer = PaginatedUserCompositionSerializer(this_page_compositions)
        return Response(data=serializer.data)

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
@permission_classes((permissions.IsAuthenticated,))
def reset_name(request, format=None):
    try:
        name = request.DATA['name']
        user = request.user
        user.name = name
        try:
            user.full_clean()
            user.save()
            ser = ExistingUserSerializer(user, context={'request': request})
            return Response(ser.data)
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def reset_about(request, format=None):
    try:
        about = request.DATA['about']
        user = request.user
        user.about = about
        try:
            user.full_clean()
            user.save()
            ser = ExistingUserSerializer(user, context={'request': request})
            return Response(ser.data)
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def reset_picture(request, format=None):
    try:
        picture = request.FILES['picture']
        user = request.user
        user.picture = picture
        try:
            user.full_clean()
            user.save()
            ser = ExistingUserSerializer(user, context={'request': request})
            return Response(ser.data)
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request, format=None):
    email = request.DATA.get('email')
    password = request.DATA.get('password')
    try:
        user = User.objects.get(email=email)
        if user.login_type == User.NATIVE:
            user = authenticate(username=email, password=password)

            if user is None:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

            if user.is_active:
                login(request, user)
                return Response(ExistingUserSerializer(user, context={'request': request}).data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_402_PAYMENT_REQUIRED)
        else:
            return Response(data={'error': 'Login via third party'}, status=status.HTTP_406_NOT_ACCEPTABLE)
    except User.DoesNotExist:
        return Response(status=status.HTTP_409_CONFLICT)
    except: 
        return Response(status=status.HTTP_400_BAD_REQUEST)


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


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def get_compositions(request, pk, format=None):
    user = get_object_or_404(User, pk=pk)
    user_compositions = user.arts.all().order_by('-id')

    page_num = request.GET.get('page', 1)
    paginator = Paginator(user_compositions, 9)

    try:
        this_page_compositions = paginator.page(page_num)
    except PageNotAnInteger:
        this_page_compositions = paginator.page(1)
    except EmptyPage:
        raise Http404

    serializer = PaginatedUserCompositionSerializer(this_page_compositions)
    return Response(data=serializer.data)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def get_interpretations(request, pk, format=None):
    user = get_object_or_404(User, pk=pk)
    user_interpretations = user.interpretation_set.all().order_by('-id')

    page_num = request.GET.get('page', 1)
    paginator = Paginator(user_interpretations, 9)

    try:
        this_page_interpretations = paginator.page(page_num)
    except PageNotAnInteger:
        this_page_interpretations = paginator.page(1)
    except EmptyPage:
        raise Http404

    serializer = PaginatedUserInterpretationSerializer(this_page_interpretations)
    return Response(data=serializer.data)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def get_uploads(request, pk, format=None):
    user = get_object_or_404(User, pk=pk)
    user_uploads = user.compositions.all().order_by('-id')

    page_num = request.GET.get('page', 1)
    paginator = Paginator(user_uploads, 9)

    try:
        this_page_compositions = paginator.page(page_num)
    except PageNotAnInteger:
        this_page_compositions = paginator.page(1)
    except EmptyPage:
        raise Http404

    serializer = PaginatedUserCompositionSerializer(this_page_compositions)
    return Response(data=serializer.data)

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
