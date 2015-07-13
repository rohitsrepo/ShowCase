from rest_framework import serializers
from .models import Post
from interpretations.models import Interpretation
from interpretations.serializers import PostInterpretationSerializer
from postVotes.serializers import VoteSerializer
from accounts.models import User
from rest_framework.pagination import PaginationSerializer
from ShowCase.serializers import URLImageField
from compositions.models import Composition

class ContentObjectRelatedField(serializers.RelatedField):

    def to_native(self, value):

        if isinstance(value, Interpretation):
            serializer = PostInterpretationSerializer(value)
        else:
            raise Exception('Unexpected type of tagged object')

        return serializer.data

class PostUserSerializer(serializers.ModelSerializer):
    picture = serializers.CharField(source='get_picture_url', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'name', 'picture', 'slug')

class PostCompositionSerializer(serializers.ModelSerializer):
    interpretations_count= serializers.CharField(source='get_interpretations_count', read_only=True)
    artist = PostUserSerializer(read_only=True)
    matter = URLImageField(source='matter')
    matter_550 = serializers.CharField(source='get_550_url', read_only=True)
    matter_350 = serializers.CharField(source='get_350_url', read_only=True)

    class Meta:
        model = Composition
        fields = ('title', 'matter', 'slug', 'matter_350', 'matter_550', 'interpretations_count', 'views', 'artist')

class PostSerializer(serializers.ModelSerializer):
    timesince = serializers.CharField(source='timesince', read_only=True)
    content = ContentObjectRelatedField(source='content_object')
    creator = PostUserSerializer(read_only=True)
    composition = PostCompositionSerializer(read_only=True)
    vote = VoteSerializer()
    comments_count = serializers.CharField(source='get_comments_count', read_only=True)
    voting_status = serializers.SerializerMethodField('get_voting_status')

    class Meta:
        model = Post
        fields = ('id', 'composition', 'creator', 'content', 'timesince', 'vote', 'comments_count', 'voting_status')

    def get_voting_status(self, obj):
        request = self.context['request']
        return obj.get_voting_status(request.user)

class PaginatedPostSerializer(PaginationSerializer):
    class Meta:
        object_serializer_class = PostSerializer