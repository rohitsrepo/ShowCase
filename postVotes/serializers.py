from rest_framework import serializers
from .models import PostVote


class VoteSerializer(serializers.ModelSerializer):
    total = serializers.CharField(source='get_total', read_only=True)

    class Meta:
        model = PostVote
        fields = ('total', 'positive', 'negative')


class VotingSerializer(serializers.ModelSerializer):
    vote = serializers.BooleanField(default=True)

    class Meta:
        model = PostVote
        fields = ('id', 'vote')
