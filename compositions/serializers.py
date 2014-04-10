from rest_framework import serializers
from .models import Composition
from django.conf import settings
from ShowCase.serializers import HyperlinkedImageField, HyperlinkedFileField

class CompositionSerializer(serializers.HyperlinkedModelSerializer):
    artist = serializers.HyperlinkedRelatedField(source='artist', read_only=True ,view_name='user-detail')
    display_image = HyperlinkedImageField(source='display_image', required=False,
	     default_url=settings.DEFAULT_COMPOSITION_IMAGE_PICTURE
	    )
    matter = HyperlinkedFileField(source='matter', default_url=None) 
    timesince = serializers.CharField(source='timesince', read_only=True)

    class Meta:
        model = Composition
        fields = ('id', 'url', 'title', 'artist', 'description', 'created', 
		 'content_type','display_image', 'matter', 'timesince'
		)
