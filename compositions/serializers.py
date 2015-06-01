from rest_framework import serializers
from .models import Composition, InterpretationImage
from ShowCase.serializers import URLImageField

class CompositionUserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    picture = URLImageField(source='picture')

    class Meta:
        model = Composition
        fields = ('id', 'full_name', 'picture')

class CompositionSerializer(serializers.ModelSerializer):
    matter = URLImageField(source='matter')
    timesince = serializers.CharField(source='timesince', read_only=True)
    uploader = CompositionUserSerializer(read_only=True)
    artist = CompositionUserSerializer(read_only=True)

    class Meta:
        model = Composition
        fields = ('id', 'title', 'artist', 'description', 'created',
		   'matter', 'timesince', 'vote', 'slug', 'uploader', 'views')
    	read_only_fields = ('slug', 'vote', 'views')

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
