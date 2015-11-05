from rest_framework import serializers
from .models import Composition, InterpretationImage
from accounts.models import User
from ShowCase.serializers import URLImageField
from rest_framework.pagination import PaginationSerializer

class CompositionUserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    picture = URLImageField(source='picture')

    class Meta:
        model = User
        fields = ('id', 'full_name', 'picture', 'slug', 'name')

class CompositionSerializer(serializers.ModelSerializer):
    matter = serializers.Field(source='matter_url')
    matter_550 = serializers.CharField(source='get_550_url', read_only=True)
    matter_400 = serializers.CharField(source='get_400_url', read_only=True)
    matter_thumbnail = serializers.CharField(source='get_thumbnail_url', read_only=True)
    matter_aspect = serializers.FloatField(source='get_matter_aspect', read_only=True)
    timesince = serializers.CharField(source='timesince', read_only=True)
    interpretations_count = serializers.CharField(source='get_interpretations_count', read_only=True)
    uploader = CompositionUserSerializer(read_only=True)
    artist = CompositionUserSerializer(read_only=True)
    is_bookmarked = serializers.SerializerMethodField('get_is_bookmarked')
    is_admired = serializers.SerializerMethodField('get_is_admired')
    bookmarks_count = serializers.CharField(source='bookmarks_count', read_only=True)
    admirers_count = serializers.CharField(source='admirers_count', read_only=True)
    buckets_count = serializers.CharField(source='buckets_count', read_only=True)
    has_ownership = serializers.SerializerMethodField('get_ownership')
    nsfw = serializers.SerializerMethodField('is_nsfw')

    class Meta:
        model = Composition
        fields = ('id', 'title', 'artist', 'description', 'created', 'major',
		   'matter', 'matter_400', 'matter_550', 'matter_thumbnail', 'matter_aspect', 'timesince', 'nsfw',
           'slug', 'uploader', 'views', 'interpretations_count', 'is_bookmarked',
           'is_admired', 'admirers_count', 'bookmarks_count', 'buckets_count', 'has_ownership')
    	read_only_fields = ('id', 'slug', 'views', 'created')

    def get_ownership(self, obj):
        request = self.context['request']
        return obj.has_ownership(request.user.id)

    def get_is_bookmarked(self, obj):
        request = self.context['request']
        return obj.is_bookmarked(request.user.id)

    def get_is_admired(self, obj):
        request = self.context['request']
        return obj.is_admired(request.user.id)

    def is_nsfw(self, obj):
        request = self.context['request']
        return obj.is_nsfw(request.user)

class PaginatedCompositionSerializer(PaginationSerializer):
    class Meta:
        object_serializer_class = CompositionSerializer


class NewCompositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Composition
        fields = ('title', 'artist', 'matter', 'nsfw', 'slug')
        read_only_fields = ('slug', )

class EditCompositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Composition
        fields = ('id', 'title', 'artist', 'nsfw', 'slug')
        read_only_fields = ('id', 'slug')

class CompositionMatterSerializer(serializers.Serializer):
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

class InterpretationImageSerializer(serializers.ModelSerializer):
    url = URLImageField(source='image', read_only=True)
    image_550 = serializers.CharField(source='get_550_url', read_only=True)
    image_400 = serializers.CharField(source='get_400_url', read_only=True)

    class Meta:
        model = InterpretationImage
        fields = ('image', 'url', 'id', 'image_550', 'image_400', 'source_type')
