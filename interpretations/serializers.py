from rest_framework import serializers

from ShowCase.serializers import URLImageField

from .models import Interpretation

from accounts.models import User
from compositions.models import Composition
from interpretationVotes.models import InterpretationVote

class InterpretationUserSerializer(serializers.ModelSerializer):
    picture = serializers.Field(source='get_picture_url')

    class Meta:
        model = User
        fields = ('id', 'name', 'picture', 'slug')

class InterpretationCompositionSerializer(serializers.ModelSerializer):
    matter = serializers.Field(source='matter_url')
    matter_400 = serializers.CharField(source='get_400_url', read_only=True)

    class Meta:
        model = Composition
        fields = ('id', 'title', 'slug', 'matter', 'matter_400', 'major')

class InterpretationVoteSerializer(serializers.ModelSerializer):
    total = serializers.CharField(source='get_total', read_only=True)

    class Meta:
        model = InterpretationVote
        fields = ('total', )

class InterpretationSerializer(serializers.ModelSerializer):
    user = InterpretationUserSerializer(read_only=True)
    composition = InterpretationCompositionSerializer(read_only=True)
    timesince = serializers.CharField(source='timesince', read_only=True)
    vote = InterpretationVoteSerializer(read_only=True)
    text = serializers.CharField(source='short_text', read_only=True)
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    is_bookmarked = serializers.SerializerMethodField('get_is_bookmarked')

    class Meta:
        model = Interpretation
        fields = ('id', 'interpretation', 'user', 'composition', 'timesince', 'is_bookmarked',
         'vote', 'text', 'slug', 'url', 'is_draft', 'title', 'updated')
        read_only_fields = ('id', 'slug')
        write_only_fields = ('is_draft', )

    def get_is_bookmarked(self, obj):
        request = self.context['request']
        return obj.is_bookmarked(request.user.id)

class PostInterpretationSerializer(serializers.ModelSerializer):
    text = serializers.CharField(source='to_text', read_only=True)

    class Meta:
        model = Interpretation
        fields = ('id', 'interpretation', 'text', 'title')
