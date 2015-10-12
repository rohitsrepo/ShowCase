from .models import User
from .serializers import NewUserSerializer, ExistingUserSerializer, PasswordUserSerializer
from .artistSerializers import PaginatedUserCompositionSerializer, PaginatedUserInterpretationSerializer
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics, permissions
from .permissions import IsHimselfOrReadOnly, IsHimself
from django.contrib.auth import authenticate, login, logout
from ShowCase.utils import check_object_permissions
from django.shortcuts import get_object_or_404, redirect
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

    next_url = request.GET.get('next', '/')
    return redirect(next_url)

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


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def get_current_user(request, format=None):
    if request.user.is_authenticated():
        return Response(ExistingUserSerializer(request.user, context={'request': request}).data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated, ))
def search_artist(request, format=None):
    if not request.user.is_authenticated():
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    query = request.GET.get('q', '')
    artists = User.objects.filter(Q(name__icontains=query))[:20]

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

    serializer = PaginatedUserCompositionSerializer(this_page_compositions, context={'request': request})
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

    serializer = PaginatedUserCompositionSerializer(this_page_compositions, context={'request': request})
    return Response(data=serializer.data)

