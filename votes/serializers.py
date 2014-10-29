from rest_framework import serializers
from .models import Vote


class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = ('positive', 'negative', 'composition')
        read_only_fields = ('positive', 'negative', 'composition')


class VotingSerializer(serializers.ModelSerializer):
    vote = serializers.BooleanField(default=True)

    class Meta:
        model = Vote
        fields = ('id', 'vote')
