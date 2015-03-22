from rest_framework import serializers
from .models import Composition
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

    class Meta:
        model = Composition
        fields = ('id', 'title', 'artist', 'description', 'created',
		   'matter', 'timesince', 'vote', 'slug', 'uploader')
	read_only_fields = ('slug', 'vote')
