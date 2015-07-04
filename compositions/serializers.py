from rest_framework import serializers
from .models import Composition, InterpretationImage
from ShowCase.serializers import URLImageField
from rest_framework.pagination import PaginationSerializer

class CompositionUserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    picture = URLImageField(source='picture')

    class Meta:
        model = Composition
        fields = ('id', 'full_name', 'picture', 'slug')

class CompositionSerializer(serializers.ModelSerializer):
    matter = URLImageField(source='matter')
    matter_550 = serializers.CharField(source='get_550_url', read_only=True)
    matter_350 = serializers.CharField(source='get_350_url', read_only=True)
    matter_aspect = serializers.FloatField(source='get_matter_aspect', read_only=True)
    timesince = serializers.CharField(source='timesince', read_only=True)
    interpretations_count = serializers.CharField(source='get_interpretations_count', read_only=True)
    uploader = CompositionUserSerializer(read_only=True)
    artist = CompositionUserSerializer(read_only=True)
    is_collected = serializers.SerializerMethodField('get_is_collected')

    class Meta:
        model = Composition
        fields = ('id', 'title', 'artist', 'description', 'created',
		   'matter', 'matter_350', 'matter_550', 'matter_aspect', 'timesince', 'vote',
           'slug', 'uploader', 'views', 'interpretations_count', 'is_collected')
    	read_only_fields = ('slug', 'vote', 'views')

    def get_is_collected(self, obj):
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
