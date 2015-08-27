from rest_framework import serializers
from rest_framework.pagination import PaginationSerializer

from .models import User

from compositions.models import Composition
from compositions.serializers import CompositionSerializer
from interpretations.models import Interpretation
from ShowCase.serializers import URLImageField

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('slug', 'name')

class PaginatedUserCompositionSerializer(PaginationSerializer):
	class Meta:
		object_serializer_class = CompositionSerializer

class UserInterpretationSerializer(serializers.ModelSerializer):
    composition = CompositionSerializer(read_only=True)
    timesince = serializers.CharField(source='timesince', read_only=True)
    interpretation = serializers.CharField(source='to_text', read_only=True)

    class Meta:
        model = Interpretation
        fields = ('composition', 'interpretation', 'timesince')

class PaginatedUserInterpretationSerializer(PaginationSerializer):
    class Meta:
        object_serializer_class = UserInterpretationSerializer