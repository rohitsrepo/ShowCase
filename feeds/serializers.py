from rest_framework import serializers
from .models import StaffPost
from rest_framework.pagination import PaginationSerializer
from compositions.models import Composition
from interpretations.models import Interpretation
from accounts.models import User
from interpretationVotes.models import InterpretationVote
from ShowCase.serializers import URLImageField

class PostUserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = ('full_name',)

class PostCompositionSerializer(serializers.ModelSerializer):
    uploader = PostUserSerializer(read_only=True)
    artist = PostUserSerializer(read_only=True)
    matter = URLImageField(source='matter')
    matter_550 = serializers.CharField(source='get_550_url', read_only=True)
    matter_350 = serializers.CharField(source='get_350_url', read_only=True)

    class Meta:
        model = Composition
        fields = ("id", "title", "matter", "artist", "slug", "uploader", "matter_350", "matter_550")

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