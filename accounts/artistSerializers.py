from rest_framework import serializers
from compositions.models import Composition
from rest_framework.pagination import PaginationSerializer
from ShowCase.serializers import URLImageField


class ArtistCompositionSerializer(serializers.ModelSerializer):
    interpretations_count= serializers.CharField(source='get_interpretations_count', read_only=True)
    matter = URLImageField(source='matter')
    matter_550 = serializers.CharField(source='get_550_url', read_only=True)
    matter_350 = serializers.CharField(source='get_350_url', read_only=True)

    class Meta:
        model = Composition
        fields = ('title', 'matter', 'slug', 'matter_350', 'matter_550', 'interpretations_count')

class PaginatedArtistCompositionSerializer(PaginationSerializer):
	class Meta:
		object_serializer_class = ArtistCompositionSerializer