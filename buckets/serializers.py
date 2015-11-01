from rest_framework import serializers
from rest_framework.pagination import PaginationSerializer

from ShowCase.serializers import URLImageField

from .models import Bucket, BucketMembership

from accounts.models import User
from compositions.models import Composition
from compositions.serializers import CompositionSerializer

class UserSerializer(serializers.ModelSerializer):
    picture = serializers.Field(source='get_picture_url')
    is_followed = serializers.SerializerMethodField('get_is_followed')

    class Meta:
        model = User
        fields = ('id', 'slug', 'name', 'picture', 'is_followed')

    def get_is_followed(self, obj):
        request = self.context['request']
        return obj.is_followed(request.user.id)

class BucketSerializer(serializers.ModelSerializer):
    compositions_count = serializers.CharField(source='compositions_count', read_only=True)
    has_background = serializers.CharField(source='has_background', read_only=True)
    background_url = serializers.CharField(source='background_url', read_only=True)
    picture = serializers.CharField(source='picture', read_only=True)
    owner = UserSerializer(read_only=True)
    has_ownership = serializers.SerializerMethodField('get_ownership')
    composition_added = serializers.SerializerMethodField('get_composition_added')
    is_bookmarked = serializers.SerializerMethodField('get_is_bookmarked')
    is_admired = serializers.SerializerMethodField('get_is_admired')
    admire_as = serializers.SerializerMethodField('get_admire_as')
    is_public = serializers.Field(source='public')

    class Meta:
        model = Bucket
        fields = ('id',
            'owner',
            'name',
            'description',
            'slug',
            'views',
            'is_public',
            'compositions_count',
            'picture',
            'has_background',
            'background_url',
            'has_ownership',
            'composition_added',
            'is_bookmarked',
            'is_admired',
            'admire_as')
        read_only_fields = ('id', 'slug', 'views' )

    def get_ownership(self, obj):
        request = self.context['request']
        return obj.has_ownership(request.user.id)

    def get_is_bookmarked(self, obj):
        request = self.context['request']
        return obj.is_bookmarked(request.user.id)

    def get_is_admired(self, obj):
        request = self.context['request']
        return obj.is_admired(request.user.id)

    def get_admire_as(self, obj):
        request = self.context['request']
        return obj.admire_as(request.user.id)

    def get_composition_added(self, obj):
        composition_id = self.context.get('composition_id', '')
        if composition_id:
            return obj.is_composition_added(composition_id)
        else:
            return None

class BucketBackgroundSerializer(serializers.Serializer):
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

class BucketCompositionSerializer(serializers.ModelSerializer):
    interpretations_count= serializers.CharField(source='get_interpretations_count', read_only=True)
    matter_aspect = serializers.FloatField(source='get_matter_aspect', read_only=True)
    artist = UserSerializer(read_only=True)
    matter = URLImageField(source='matter')
    matter_550 = serializers.CharField(source='get_550_url', read_only=True)
    matter_400 = serializers.CharField(source='get_400_url', read_only=True)
    is_bookmarked = serializers.SerializerMethodField('get_is_bookmarked')
    bookmarks_count = serializers.CharField(source='bookmarks_count')

    class Meta:
        model = Composition
        fields = ('id', 'title', 'matter', 'slug', 'matter_400', 'matter_550', 'interpretations_count',
         'views', 'artist', 'matter_aspect', 'is_bookmarked', 'bookmarks_count')

    def get_is_bookmarked(self, obj):
        request = self.context['request']
        return obj.is_bookmarked(request.user.id)

class PaginatedBucketCompositionSerializer(PaginationSerializer):
    class Meta:
        object_serializer_class = BucketCompositionSerializer

class BucketMembershipSerializer(serializers.ModelSerializer):
    composition = CompositionSerializer(read_only=True)

    class Meta:
        model = BucketMembership
        fields = ('bucket', 'composition', 'description', 'added')
        read_only_fields = ('bucket', 'added')

class BucketMembershipCreateSerializer(serializers.Serializer):
    composition_id = serializers.IntegerField(required=True)
    description = serializers.CharField(max_length=500, required=False, default="")