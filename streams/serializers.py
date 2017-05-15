from rest_framework import serializers

from posts.models import Post

from accounts.models import User
from accounts.serializers import ExistingUserSerializer
from buckets.models import Bucket
from buckets.serializers import BucketSerializer
from compositions.models import Composition
from compositions.serializers import CompositionSerializer
from interpretations.models import Interpretation
from interpretations.serializers import InterpretationSerializer

class ContentObjectRelatedField(serializers.RelatedField):

    def to_native(self, value):

        print value
        verb = value[0]['verb']

        if verb in [Post.INTERPRET, Post.ADMIRE_INTERPRET]:
            interpretation_id = value[0]['object']
            interpretation = Interpretation.objects.get(pk=interpretation_id)
            serializer = InterpretationSerializer(interpretation, context={'request': self.context['request']})
        elif verb in [Post.CREATE, Post.ADMIRE_ART, Post.ADD]:
            composition_id = value[0]['object']
            composition = Composition.objects.get(pk=composition_id)
            serializer = CompositionSerializer(composition, context={'request': self.context['request']})
        elif verb in [Post.ADMIRE_BUCKET, Post.BUCKET]:
            interpretation_id = value[0]['object']
            bucket = Bucket.objects.get(pk=bucket_id)
            serializer = BucketSerializer(bucket, context={'request': self.context['request']})
        elif verb=='FL':
            return {};
        else:
            print value
            raise Exception('Unexpected type of notification activity')

        return serializer.data

class TargetObjectRelatedField(serializers.RelatedField):

    def to_native(self, value):

        print value
        verb = value[0]['verb']

        if verb in [Post.INTERPRET, Post.BUCKET]:
            composition_id = value[0]['target']
            composition = Composition.objects.get(pk=composition_id)
            serializer = CompositionSerializer(composition, context={'request': self.context['request']})
        elif verb in ['FL', Post.ADMIRE_INTERPRET, Post.ADMIRE_BUCKET, Post.BUCKET, Post.CREATE, Post.ADMIRE_ART]:
            return {};
        else:
            print value
            raise Exception('Unexpected type of notification activity')

        return serializer.data

class NotificationSerializer(serializers.Serializer):
    verb = serializers.CharField(max_length=4, source='verb')
    actors = serializers.CharField(max_length=4, source='activities')
    content_object = ContentObjectRelatedField(source='activities')
    target_object = TargetObjectRelatedField(source='activities')
    id = serializers.CharField(max_length=32, read_only=True)
    is_read = serializers.BooleanField(read_only=True)
    is_seen = serializers.BooleanField(read_only=True)
    activity_count = serializers.IntegerField(read_only=True)
    actor_count = serializers.IntegerField(read_only=True)
    group = serializers.CharField(max_length=32, read_only=True)

    def transform_actors(self, obj, value):
        actors = [activity['actor'] for activity in value]
        actor_objects = User.objects.filter(id__in=actors)
        return ExistingUserSerializer(actor_objects, context=self.context).data
