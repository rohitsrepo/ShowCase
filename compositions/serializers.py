from rest_framework import serializers
from .models import Composition
from django.conf import settings
from ShowCase.serializers import HyperlinkedImageField, HyperlinkedFileField, URLImageField
from rest_framework.exceptions import ParseError


class TagListSerializer(serializers.WritableField):
    
    def from_native(self, data):
        if type(data) is not list:
            raise ParseError("Expected a list of data")    
        return data

    def to_native(self, obj):
        if type(obj) is not list:
            return [tag.name for tag in obj.all()]
        return obj



class CompositionSerializer(serializers.ModelSerializer):
    #artist = serializers.HyperlinkedRelatedField(source='artist', read_only=True, view_name='user-detail')
    #display_image = HyperlinkedImageField(source='display_image', required=False, default_url=settings.DEFAULT_COMPOSITION_IMAGE_PICTURE)
    matter = URLImageField(source='matter')
    timesince = serializers.CharField(source='timesince', read_only=True)
    tags = TagListSerializer(required=False)

    class Meta:
        model = Composition
        fields = ('id', 'title', 'artist', 'description', 'created',
		   'matter', 'timesince', 'vote', 'slug', 'tags')
	read_only_fields = ('artist', 'slug', 'vote')
	depth =1 
