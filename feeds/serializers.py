from rest_framework import serializers
from rest_framework.pagination import PaginationSerializer

from .models import StaffPost, Fresh

from ShowCase.serializers import URLImageField

from accounts.models import User
from buckets.models import Bucket
from buckets.serializers import BucketSerializer
from compositions.models import Composition
from compositions.serializers import CompositionSerializer
from interpretations.models import Interpretation
from interpretationVotes.models import InterpretationVote

class PostUserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = ('full_name', 'slug')

class PostCompositionSerializer(serializers.ModelSerializer):
    uploader = PostUserSerializer(read_only=True)
    artist = PostUserSerializer(read_only=True)
    matter = URLImageField(source='matter')
    matter_550 = serializers.CharField(source='get_550_url', read_only=True)
    matter_400 = serializers.CharField(source='get_400_url', read_only=True)

    class Meta:
        model = Composition
        fields = ("id", "title", "matter", "artist", "slug", "uploader", "matter_400", "matter_550", "views")

class PostInterpretationVoteSerializer(serializers.ModelSerializer):
    total = serializers.CharField(source='get_total', read_only=True)

    class Meta:
        model = InterpretationVote
        fields = ('total', )

class PostInterpretationSerializer(serializers.ModelSerializer):
    vote = PostInterpretationVoteSerializer(read_only=True)
    timesince = serializers.CharField(source='timesince', read_only=True)
    user = PostUserSerializer(read_only=True)
    interpretation = serializers.CharField(source='to_text', read_only=True)

    class Meta:
        model = Interpretation
        fields = ("id", "interpretation", "user", 'vote', 'timesince')

class PostSerializer(serializers.ModelSerializer):
    composition = PostCompositionSerializer(read_only=True)
    interpretation = PostInterpretationSerializer(read_only=True)
    search_parameter = serializers.CharField(source='get_search_parameter', read_only=True)

    class Meta:
        model = StaffPost
        fields = ('composition', 'interpretation', 'id', 'search_parameter')

class PaginatedPostSerializer(PaginationSerializer):
    """
    Serializes page objects of user querysets.
    """
    class Meta:
        object_serializer_class = PostSerializer

class ContentObjectRelatedField(serializers.RelatedField):

    def to_native(self, value):

        if isinstance(value, Bucket):
            serializer = BucketSerializer(value, context={'request': self.context['request']})
        elif isinstance(value, Composition):
            serializer = CompositionSerializer(value, context={'request': self.context['request']})
        else:
            raise Exception('Unexpected type of tagged object')

        return serializer.data

class FeedPostSerializer(serializers.ModelSerializer):
    content = ContentObjectRelatedField(source='content_object')

    class Meta:
        model = Fresh
        fields = ('id', 'content', 'feed_type',)

class PaginatedFeedPostSerializer(PaginationSerializer):

    class Meta:
        object_serializer_class = FeedPostSerializer