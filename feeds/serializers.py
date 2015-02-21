from rest_framework import serializers
from .models import StaffPost
from rest_framework.pagination import PaginationSerializer
from compositions.models import Composition
from interpretations.models import Interpretation


class PostCompositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Composition
        fields = ("id", "title", "matter", "artist")

class PostInterpretationSerializer(serializers.ModelSerializer):

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