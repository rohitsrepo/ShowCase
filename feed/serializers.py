from rest_framework import serializers
from .models import FeedPost
from ShowCase.serializers import URLImageField
from rest_framework.pagination import PaginationSerializer

class FeedPostSerializer(serializers.ModelSerializer):
    painting_image = URLImageField(source='painting_image')

    class Meta:
        model = FeedPost
        fields = ('id', 'painting_image', 'painting_name', 'painter', 'interpretation', 'interpretation_writer', 'interpretation_votes')	
        
        
        
class PaginatedFeedPostSerializer(PaginationSerializer):
    #Serializes page objects of user querysets.

    class Meta:
        object_serializer_class = FeedPostSerializer