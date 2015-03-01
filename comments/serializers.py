from rest_framework import serializers
from .models import Comment
from accounts.models import User
from ShowCase.serializers import URLImageField


class CommenterSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    picture = URLImageField(source='picture')

    class Meta:
        model = User
        fields = ('id', 'full_name', 'picture')

class CommentSerializer(serializers.ModelSerializer):
    timesince = serializers.CharField(source='timesince', read_only=True)
    commenter = CommenterSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'comment', 'commenter', 'edited', 'timesince')
        read_only_fields = ('id', 'edited')
