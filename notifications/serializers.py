from rest_framework import serializers
from .models import Notification

class GenericRelatedField(serializers.RelatedField):
    """
    Custom field to handle the generic relations
    """

    def to_native(self, value):
	return {'obj': unicode(value), 'url': value.get_absolute_url()}

class NotificationSerializer(serializers.ModelSerializer):
    timesince = serializers.DateTimeField(source='timesince')
    actor = GenericRelatedField(read_only=True)
    action_object = GenericRelatedField(read_only=True)
    target = GenericRelatedField(read_only=True)

    class Meta:
	model = Notification
	fields = ('id', 'recipient', 'unread', 'actor', 'verb', 'timesince', 'target', 'action_object') 
