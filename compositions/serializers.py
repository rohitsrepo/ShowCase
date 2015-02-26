from rest_framework import serializers
from .models import Composition
from ShowCase.serializers import URLImageField

class CompositionUserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = Composition
        fields = ('id', 'full_name')

class CompositionSerializer(serializers.ModelSerializer):
    matter = URLImageField(source='matter')
    timesince = serializers.CharField(source='timesince', read_only=True)
    artist = CompositionUserSerializer(read_only=True)

    class Meta:
        model = Composition
        fields = ('id', 'title', 'artist', 'description', 'created',
		   'matter', 'timesince', 'vote', 'slug')
	read_only_fields = ('slug', 'vote')
