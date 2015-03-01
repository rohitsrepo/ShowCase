from rest_framework import serializers
from .models import InterpretationVote


class VoteSerializer(serializers.ModelSerializer):
    total = serializers.CharField(source='get_total', read_only=True)

    class Meta:
        model = InterpretationVote
        fields = ('total', )


class VotingSerializer(serializers.ModelSerializer):
    vote = serializers.BooleanField(default=True)

    class Meta:
        model = InterpretationVote
        fields = ('id', 'vote')
