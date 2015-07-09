from rest_framework import serializers
from .models import PostComment
from accounts.models import User


class CommenterSerializer(serializers.ModelSerializer):
    picture = serializers.CharField(source='get_picture_url', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'name', 'picture')

class CommentSerializer(serializers.ModelSerializer):
    timesince = serializers.CharField(source='timesince', read_only=True)
    commenter = CommenterSerializer(read_only=True)

    class Meta:
        model = PostComment
        fields = ('id', 'comment', 'commenter', 'edited', 'timesince')
        read_only_fields = ('id', 'edited')
