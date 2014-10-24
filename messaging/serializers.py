from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    timesince = serializers.CharField(source='timesince', read_only=True)

    class Meta:
        model = Message
        fields = (
            'id', 'sender', 'subject', 'body', 'read', 'timesince')
        read_only_fields = ('id', 'read')
