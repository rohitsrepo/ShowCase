from rest_framework import serializers
from accounts.models import User
from compositions.models import Composition
from interpretations.models import Interpretation
from rest_framework.pagination import PaginationSerializer
from ShowCase.serializers import URLImageField

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('slug', 'name')

class UserCompositionSerializer(serializers.ModelSerializer):
    interpretations_count= serializers.CharField(source='get_interpretations_count', read_only=True)
    matter_aspect = serializers.FloatField(source='get_matter_aspect', read_only=True)
    artist = UserSerializer(read_only=True)
    matter = URLImageField(source='matter')
    matter_550 = serializers.CharField(source='get_550_url', read_only=True)
    matter_350 = serializers.CharField(source='get_350_url', read_only=True)
    is_bookmarked = serializers.SerializerMethodField('get_is_bookmarked')
    bookmarks_count = serializers.CharField(source='bookmarks_count')

    class Meta:
        model = Composition
        fields = ('id', 'title', 'matter', 'slug', 'matter_350', 'matter_550', 'interpretations_count', 'views', 'artist', 'matter_aspect',
            'is_bookmarked', 'bookmarks_count')
        
    def get_is_bookmarked(self, obj):
        request = self.context['request']
        return obj.is_bookmarked(request.user.id)

class PaginatedUserCompositionSerializer(PaginationSerializer):
	class Meta:
		object_serializer_class = UserCompositionSerializer

class UserInterpretationSerializer(serializers.ModelSerializer):
    composition = UserCompositionSerializer(read_only=True)
    timesince = serializers.CharField(source='timesince', read_only=True)
    interpretation = serializers.CharField(source='to_text', read_only=True)

    class Meta:
        model = Interpretation
        fields = ('composition', 'interpretation', 'timesince')

class PaginatedUserInterpretationSerializer(PaginationSerializer):
    class Meta:
        object_serializer_class = UserInterpretationSerializer