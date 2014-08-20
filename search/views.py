from django.shortcuts import render
from django.db.models import Q
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.compat import BytesIO
from compositions.models import Composition
from compositions.serializers import CompositionSerializer
from accounts.models import User
from accounts.serializers import NewUserSerializer
from tagging.models import Tag
from tagging.serializers import TagSerializer

# Create your views here.

class SearchDetail(APIView):
    def get(self, request, format=None):
        query = request.DATA['query']
        users = User.objects.get(Q(first_name__contains='lily') | Q(last_name__contains='lily'))
        compositions = Composition.objects.get(title__contains = query)
        tags = Tag.objects.get(tag_name__contains= query)

        user_ser = NewUserSerializer(User, many = True, context={'request': request})
        composition_ser = CompositionSerializer(Composition, many = True, context={'request': request})
        tag_ser = TagSerializer(Tag, many = True, context={'request': request})
        
        ser_data = {
            'USER' : user_json,
            'COMPOSITION' : composition_json,
            'TAG' : tag_json
            }
        Response(ser_data)
        
        
        
        