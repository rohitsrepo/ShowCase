from rest_framework import serializers
from .models import Message
from django.conf import settings

class MessageSerializer(serializers.HyperlinkedModelSerializer):
    #recipient = serializers.HyperlinkedRelatedField(source='recipient', read_only=True, view_name='user-detail')
    class Meta:
	model = Message
	fields = ('id', 'sender', 'recipient', 'subject', 'body', 'read', 'created')