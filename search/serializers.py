from rest_framework import serializers
from rest_framework.pagination import PaginationSerializer

from accounts.models import User
from accounts.serializers import ExistingUserSerializer
from buckets.models import Bucket
from buckets.serializers import BucketSerializer
from compositions.models import Composition
from compositions.serializers import CompositionSerializer

class ObjectRelatedField(serializers.RelatedField):

    def to_native(self, value):

        if isinstance(value, User):
            serializer = ExistingUserSerializer(value, context={'request': self.context['request']})
        elif isinstance(value, Composition):
            serializer = CompositionSerializer(value, context={'request': self.context['request']})
        elif isinstance(value, Bucket):
            serializer = BucketSerializer(value, context={'request': self.context['request']})
        else:
            raise Exception('Unexpected type of search result object')

        return serializer.data

class SearchSerializer(serializers.Serializer):
    content_type = serializers.Field(source='model_name')
    content_object = ObjectRelatedField(source='object')


class PaginatedSearchSerializer(PaginationSerializer):
    class Meta:
        object_serializer_class = SearchSerializer