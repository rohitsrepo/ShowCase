from rest_framework import serializers
from .models import Composition
from django.conf import settings
from ShowCase.serializers import HyperlinkedImageField, HyperlinkedFileField, URLImageField


class CompositionSerializer(serializers.ModelSerializer):
    #artist = serializers.HyperlinkedRelatedField(source='artist', read_only=True, view_name='user-detail')
    #display_image = HyperlinkedImageField(source='display_image', required=False, default_url=settings.DEFAULT_COMPOSITION_IMAGE_PICTURE)
    matter = URLImageField(source='matter')
    timesince = serializers.CharField(source='timesince', read_only=True)

    class Meta:
        model = Composition
        fields = ('id', 'title', 'artist', 'description', 'created',
		   'matter', 'timesince', 'vote', 'slug', 'tags')
	read_only_fields = ('artist', 'slug', 'vote')
	depth =1 
