from rest_framework import serializers
from .models import StaffPost
from rest_framework.pagination import PaginationSerializer
from compositions.models import Composition
from interpretations.models import Interpretation
from accounts.models import User

class PostUserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = ('full_name',)

class PostCompositionSerializer(serializers.ModelSerializer):
    artist = PostUserSerializer(read_only=True)

    class Meta:
        model = Composition
        fields = ("id", "title", "matter", "artist", "slug")

class PostInterpretationSerializer(serializers.ModelSerializer):
    user = PostUserSerializer(read_only=True)

    class Meta:
        model = Interpretation
        fields = ("id", "interpretation", "user")

class PostSerializer(serializers.ModelSerializer):
    composition = PostCompositionSerializer(read_only=True)
    interpretation = PostInterpretationSerializer(read_only=True)

    class Meta:
        model = StaffPost
        fields = ('composition', 'interpretation')
        depth=2

class PaginatedPostSerializer(PaginationSerializer):
    """
    Serializes page objects of user querysets.
    """
    class Meta:
        object_serializer_class = PostSerializer