from rest_framework import serializers
from .models import Comment 

class CommentSerializer(serializers.HyperlinkedModelSerializer):
    timesince = serializers.CharField(source='timesince', read_only=True)   
    class Meta:
	model = Comment
	fields = ('id', 'comment', 'created', 'commenter', 'composition','edited', 'timesince')
	read_only_fields = ('id', 'created', 'commenter', 'composition', 'edited')
