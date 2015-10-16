from rest_framework import serializers
from .models import User
from django.forms import widgets
from django.contrib.auth.hashers import make_password
from rest_framework.pagination import PaginationSerializer


class NewUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128, widget=widgets.PasswordInput, write_only=True)
    picture = serializers.ImageField(source='picture', required=False)

    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'about', 'password', 'picture', 'login_type')

    def save_object(self, obj, *args, **kwargs):
        # Encrypting password before saving it.
        obj.password = make_password(obj.password)
        super(NewUserSerializer, self).save_object(obj, *args, **kwargs)


class ExistingUserSerializer(serializers.ModelSerializer):
    picture = serializers.Field(source='get_picture_url')
    followers_count = serializers.Field(source='followers_count')
    paintings_count = serializers.Field(source='paintings_count')
    uploads_count = serializers.Field(source='uploads_count')
    buckets_count = serializers.Field(source='buckets_count')
    drafts_count = serializers.Field(source='drafts_count')
    is_followed = serializers.SerializerMethodField('get_is_followed')

    class Meta:
        model = User
        fields = ('id', 'email','name', 'about', 'picture', 'slug', 'nsfw', 'buckets_count', 'drafts_count', 'followers_count', 'paintings_count', 'uploads_count', 'is_followed')

    def get_is_followed(self, obj):
        request = self.context['request']
        return obj.is_followed(request.user.id)


class PaginatedUserSerializer(PaginationSerializer):
    class Meta:
        object_serializer_class = ExistingUserSerializer

class PasswordUserSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128)
    new_password = serializers.CharField(max_length=128)

    def __init__(self, *args, **kwargs):
        super(PasswordUserSerializer, self).__init__(*args, **kwargs)

        try:
            self.user = self.context['user']
        except KeyError:
            raise Exception("Please pass user as context instance")

    def validate_old_password(self, attrs, source):
        '''
        Validate the old password is valid.
        '''

        old_password = attrs[source]
        if self.user.check_password(old_password):
            return attrs
        else:
            raise serializers.ValidationError(
                "Old password that you entered is not a valid password")

class ProfilePictureSerializer(serializers.Serializer):
    upload_type = serializers.CharField(max_length=3);
    upload_image = serializers.ImageField(required=False)
    upload_url = serializers.URLField(required=False)

    def validate_upload_type(self, attrs, value):
        field_value = attrs[value]
        if (field_value == 'upl' or field_value=='url'):
            return attrs
        raise serializers.ValidationError('Upload type should be upl or url');

    def validate(self, data):
        if (data['upload_type'] == 'upl'):
            if ('upload_image' not in data.keys() or not data['upload_image']):
                raise serializers.ValidationError('Upload image can not be empty')
        elif (data['upload_type'] == 'url'):
            if ('upload_url' not in data.keys() or not data['upload_url']):
                raise serializers.ValidationError('Upload url can not be empty')

        return data
