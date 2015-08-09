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
    matter = URLImageField(source='matter')
    matter_550 = serializers.CharField(source='get_550_url', read_only=True)
    matter_350 = serializers.CharField(source='get_350_url', read_only=True)
    matter_aspect = serializers.FloatField(source='get_matter_aspect', read_only=True)
    timesince = serializers.CharField(source='timesince', read_only=True)
    interpretations_count = serializers.CharField(source='get_interpretations_count', read_only=True)
    uploader = CompositionUserSerializer(read_only=True)
    artist = CompositionUserSerializer(read_only=True)
    is_bookmarked = serializers.SerializerMethodField('get_is_bookmarked')
    bookmarks_count = serializers.CharField(source='bookmarks_count')
    buckets_count = serializers.CharField(source='buckets_count')

    class Meta:
        model = Composition
        fields = ('id', 'title', 'artist', 'description', 'created',
		   'matter', 'matter_350', 'matter_550', 'matter_aspect', 'timesince', 'vote',
           'slug', 'uploader', 'views', 'interpretations_count', 'is_bookmarked', 'bookmarks_count', 'buckets_count')
    	read_only_fields = ('slug', 'vote', 'views')

    def get_is_bookmarked(self, obj):
        request = self.context['request']
        return obj.is_bookmarked(request.user.id)

class PaginatedCompositionSerializer(PaginationSerializer):
    class Meta:
        object_serializer_class = CompositionSerializer


class NewCompositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Composition
        fields = ('title', 'artist', 'description', 'matter', 'slug')
        read_only_fields = ('slug',)

class InterpretationImageSerializer(serializers.ModelSerializer):
    url = URLImageField(source='image', read_only=True)
    image_550 = serializers.CharField(source='get_550_url', read_only=True)
    image_350 = serializers.CharField(source='get_350_url', read_only=True)

    class Meta:
        model = InterpretationImage
        fields = ('image', 'url', 'id', 'image_550', 'image_350', 'source_type')

class BookmarkerSerializer(serializers.ModelSerializer):
    picture = serializers.Field(source='get_picture_url')
    followers_count = serializers.Field(source='followers_count')
    paintings_count = serializers.Field(source='paintings_count')
    uploads_count = serializers.Field(source='uploads_count')
    is_followed = serializers.SerializerMethodField('get_is_followed')

    class Meta:
        model = User
        fields = ('id', 'slug', 'picture', 'name', 'followers_count', 'paintings_count', 'uploads_count', 'is_followed')

    def get_is_followed(self, obj):
        request = self.context['request']
        return obj.is_followed(request.user.id)