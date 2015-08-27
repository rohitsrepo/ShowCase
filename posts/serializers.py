from rest_framework import serializers
from rest_framework.pagination import PaginationSerializer

from .models import Post

from accounts.models import User
from accounts.serializers import ExistingUserSerializer
from buckets.models import Bucket
from buckets.serializers import BucketSerializer
from compositions.models import Composition
from compositions.serializers import CompositionSerializer
from interpretations.models import Interpretation
from interpretations.serializers import PostInterpretationSerializer
from postVotes.serializers import VoteSerializer
from ShowCase.serializers import URLImageField

class ContentObjectRelatedField(serializers.RelatedField):

    def to_native(self, value):

        if isinstance(value, Interpretation):
            serializer = PostInterpretationSerializer(value, context={'request': self.context['request']})
        elif isinstance(value, Composition):
            serializer = CompositionSerializer(value, context={'request': self.context['request']})
        elif isinstance(value, Bucket):
            serializer = BucketSerializer(value, context={'request': self.context['request']})
        else:
            raise Exception('Unexpected type of tagged object')

        return serializer.data

class PostSerializer(serializers.ModelSerializer):
    timesince = serializers.CharField(source='timesince', read_only=True)
    content = ContentObjectRelatedField(source='content_object')
    creator = ExistingUserSerializer(read_only=True)
    composition = CompositionSerializer(read_only=True)
    vote = VoteSerializer()
    comments_count = serializers.CharField(source='get_comments_count', read_only=True)
    voting_status = serializers.SerializerMethodField('get_voting_status')

    class Meta:
        model = Post
        fields = ('id', 'composition', 'creator', 'content', 'post_type', 'timesince', 'vote', 'comments_count', 'voting_status')

    def get_voting_status(self, obj):
        request = self.context['request']
        return obj.get_voting_status(request.user)

class PaginatedPostSerializer(PaginationSerializer):
    class Meta:
        object_serializer_class = PostSerializer