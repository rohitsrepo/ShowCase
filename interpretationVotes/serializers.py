from rest_framework import serializers
from .models import InterpretationVote


class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = InterpretationVote
        fields = ('positive', 'negative', 'interpretation')
        read_only_fields = ('positive', 'negative', 'interpretation')


class VotingSerializer(serializers.ModelSerializer):
    vote = serializers.BooleanField(default=True)

    class Meta:
        model = InterpretationVote
        fields = ('id', 'vote')
