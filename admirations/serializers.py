from rest_framework import serializers
from rest_framework.pagination import PaginationSerializer

from .models import Admiration

from accounts.serializers import ExistingUserSerializer
from compositions.models import Composition
from compositions.serializers import CompositionSerializer
from buckets.models import Bucket
from buckets.serializers import BucketSerializer

class ContentObjectRelatedField(serializers.RelatedField):

    def to_native(self, value):

        if isinstance(value, Composition):
            serializer = CompositionSerializer(value, context={'request': self.context['request']})
        elif isinstance(value, Bucket):
            serializer = BucketSerializer(value, context={'request': self.context['request']})
        else:
            raise Exception('Unexpected type of admiration object')

        return serializer.data

class AdmirationSerializer(serializers.ModelSerializer):
    content = ContentObjectRelatedField(source='content_object')
    owner = ExistingUserSerializer(read_only=True)

    class Meta:
        model = Admiration
        fields = ('id', 'owner', 'created', 'admire_type', 'content')

class PaginatedAdmirationSerializer(PaginationSerializer):
    class Meta:
        object_serializer_class = AdmirationSerializer


class AdmirationContentCreateSerializer(serializers.Serializer):
    admire_type = serializers.CharField(max_length=2)
    object_id = serializers.IntegerField()

    def validate_admire_type(self, attrs, value):
        field_value = attrs[value]
        if (field_value == Admiration.ART or field_value==Admiration.BUCKET):
            return attrs
        raise serializers.ValidationError('Invalid admire type received');