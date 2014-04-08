from rest_framework import serializers
from .models import Vote

class VoteSerializer(serializers.HyperlinkedModelSerializer):
    positive = serializers.IntegerField(source='positive', read_only=True)
    negative = serializers.IntegerField(source='negative', read_only=True)
    composition = serializers.HyperlinkedRelatedField(source='composition', read_only=True, 
	     view_name='composition-detail'
	    )

    class Meta:
	model = Vote
	fields = ('positive', 'negative', 'composition') 
	
class VotingSerializer(serializers.ModelSerializer):
    vote = serializers.BooleanField(default=True)

    class Meta:
	model = Vote
	fields = ('id','vote') 
