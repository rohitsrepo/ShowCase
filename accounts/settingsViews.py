import urllib2

from django.core.exceptions import ValidationError
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework import permissions

from .models import User, MailOptions
from .serializers import ExistingUserSerializer, PasswordUserSerializer, ProfilePictureSerializer, MailOptionsSerializer

from ShowCase.utils import check_object_permissions


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
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
def reset_nsfw(request, format=None):
    try:
        nsfw = request.DATA['nsfw']
        user = request.user
        user.nsfw = nsfw
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
        picture_ser = ProfilePictureSerializer(data=request.DATA, files=request.FILES, context={'request': request})
        if picture_ser.is_valid():
            update_picture(request.user, picture_ser.object)
            return Response(status=status.HTTP_201_CREATED)

        return Response(data=back_ser.errors, status=status.HTTP_400_BAD_REQUEST)
    except:
        raise;
        return Response(status=status.HTTP_400_BAD_REQUEST)

def get_image_from_web(image_url):
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(urllib2.urlopen(image_url).read())
        img_temp.flush()

        return img_temp

def get_image_from_upload(image_file):
    dest = NamedTemporaryFile(delete=True)
    for chunk in image_file.chunks():
        dest.write(chunk)
    return dest

def update_picture(user, upload_object):
    if (upload_object['upload_type'] == 'url'):
        image_file = get_image_from_web(upload_object['upload_url'])
    elif (upload_object['upload_type'] == 'upl'):
        image_file = get_image_from_upload(upload_object['upload_image'])

    user.picture = File(image_file)
    user.save();


class MailOptionsDetail(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, format=None):
        mailOptions = MailOptions.objects.get(user=request.user)
        ser = MailOptionsSerializer(mailOptions)
        return Response(ser.data)

    def put(self, request, format=None):
        mailOptions = MailOptions.objects.get(user=request.user)
        ser = MailOptionsSerializer(mailOptions, data=request.DATA, context={'request': request})
        if ser.is_valid():
            ser.save()
            return Response(ser.data)

        return Response(data=ser.errors, status=status.HTTP_400_BAD_REQUEST)
