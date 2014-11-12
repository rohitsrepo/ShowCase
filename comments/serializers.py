from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    timesince = serializers.CharField(source='timesince', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'comment', 'commenter',
                  'interpretation', 'edited', 'timesince')
        read_only_fields = (
            'id', 'commenter', 'interpretation', 'edited')
