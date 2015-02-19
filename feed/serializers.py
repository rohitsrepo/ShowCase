from rest_framework import serializers
from .models import TempFeedPosts
from ShowCase.serializers import URLImageField
from rest_framework.pagination import PaginationSerializer

class TempFeedPostsSerializer(serializers.ModelSerializer):
    painting_image = URLImageField(source='painting_image')

    class Meta:
        model = TempFeedPosts
        fields = ('id', 'painting_image', 'painting_name', 'painter', 'interpretation', 'interpretation_writer', 'interpretation_votes')	
        
        

class PaginatedTempFeedPostsSerializer(PaginationSerializer):
    #Serializes page objects of user querysets.

    class Meta:
        object_serializer_class = TempFeedPostsSerializer