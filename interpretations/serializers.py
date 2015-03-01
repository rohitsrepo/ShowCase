from rest_framework import serializers
from .models import Interpretation
from accounts.models import User
from interpretationVotes.models import InterpretationVote

class InterpretationUserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'full_name')

class InterpretationVoteSerializer(serializers.ModelSerializer):
    total = serializers.CharField(source='get_total', read_only=True)

    class Meta:
        model = InterpretationVote
        fields = ('total', )

class InterpretationSerializer(serializers.ModelSerializer):
    user = InterpretationUserSerializer(read_only=True)
    timesince = serializers.CharField(source='timesince', read_only=True)
    vote = InterpretationVoteSerializer(read_only=True)

    class Meta:
        model = Interpretation
        fields = ('id', 'interpretation', 'user', 'composition', 'timesince', 'vote')
        read_only_fields = ('id', 'composition')
