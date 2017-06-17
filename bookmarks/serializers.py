from rest_framework import serializers
from rest_framework.pagination import PaginationSerializer

from .models import BookMark

from accounts.serializers import ExistingUserSerializer
from compositions.models import Composition
from compositions.serializers import CompositionSerializer
from buckets.models import Bucket
from buckets.serializers import BucketSerializer
from interpretations.models import Interpretation
from interpretations.serializers import InterpretationSerializer

class ContentObjectRelatedField(serializers.RelatedField):

    def to_native(self, value):

        if isinstance(value, Composition):
            serializer = CompositionSerializer(value, context={'request': self.context['request']})
        elif isinstance(value, Bucket):
            serializer = BucketSerializer(value, context={'request': self.context['request']})
        elif isinstance(value, Interpretation):
            serializer = InterpretationSerializer(value, context={'request': self.context['request']})
        else:
            raise Exception('Unexpected type of bookmark object')

        return serializer.data

class BookmarkSerializer(serializers.ModelSerializer):
    content = ContentObjectRelatedField(source='content_object')
    owner = ExistingUserSerializer(read_only=True)
    content_type = serializers.CharField(source='bookmark_type', read_only=True)

    class Meta:
        model = BookMark
        fields = ('id', 'owner', 'created', 'content_type', 'content')

class PaginatedBookmarkSerializer(PaginationSerializer):
    class Meta:
        object_serializer_class = BookmarkSerializer


class BookmarkContentCreateSerializer(serializers.Serializer):
    content_type = serializers.CharField(max_length=2)
    object_id = serializers.IntegerField()

    def validate_content_type(self, attrs, value):
        field_value = attrs[value]
        if (field_value in [BookMark.ART, BookMark.BUCKET, BookMark.INTERPRET]):
            return attrs
        raise serializers.ValidationError('Invalid bookmark type received');