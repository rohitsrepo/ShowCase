import urllib2

from django.core.exceptions import ValidationError
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework import permissions

from .models import User, MailOptions
from .serializers import ExistingUserSerializer, PasswordUserSerializer, SetPasswordSerializer, ProfilePictureSerializer, MailOptionsSerializer
from .tasks import send_reset_password_mail

from ShowCase.utils import check_object_permissions
from compositions.colorTools import colorz


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def reset_password(request, format=None):

    serializer = PasswordUserSerializer(data=request.DATA)

    if serializer.is_valid():
        user = get_object_or_404(User, email=serializer.data['email'])

        if not user.is_active:
            return Response(data={'error': 'User account is not active'}, status=status.HTTP_400_BAD_REQUEST)


        base_url = 'http://thirddime.com/reset-password-confirm/'
        reset_url = base_url + urlsafe_base64_encode(force_bytes(user.pk)) + '-' + default_token_generator.make_token(user) + '/' 

        send_reset_password_mail.delay(user.id, reset_url)

        return Response(status=status.HTTP_200_OK)
    else:
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def reset_password_confirm(request, uidb64, token, format=None):

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        serializer = SetPasswordSerializer(data=request.DATA)
        if serializer.is_valid():
            user.set_password(serializer.data['password'])
            user.save()
            return Response()

    return Response(status=status.HTTP_400_BAD_REQUEST)

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
    user.save()
    major = colorz(user.picture.path)
    user.picture_major = major[0]
    user.save()


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
