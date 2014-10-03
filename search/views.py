from django.shortcuts import render
from compositions.models import Composition
from compositions.serializers import CompositionSerializer
from accounts.models import User
from accounts.serializers import NewUserSerializer
from haystack.query import SearchQuerySet


def queryset_gen(search_qs):
    queryResult=[]
    for item in search_qs:
        queryResult.append(item)
    return queryResult

# Create your views here.
class SearchList(APIView):
    def get(self, request, format=None):
        query = request.DATA['query']
        sqs=SearchQuerySet()
        users = queryset_gen(sqs.models(User).filter(text__contains=query))
        compositions = queryset_gen(sqs.models(Composition).filter(text__contains=query))
        
        user_ser = NewUserSerializer(users, many = True, context={'request': request})
        composition_ser = CompositionSerializer(compositions, many = True, context={'request': request})        
        
        ser_data = {
            'USERS' : user_ser.data,
            'COMPOSITIONS' : composition_ser.data
        }
        return Response(ser_data)        
 
        
def autocomplete(request):
    sqs = SearchQuerySet()
    users = queryset_gen(sqs.models(User).autocomplete(content_auto=request.GET.get('q', ''))[:3])
    compositions = queryset_gen(sqs.models(Composition).autocomplete(content_auto=request.GET.get('q', ''))[:3])
            
    user_ser = NewUserSerializer(users, many = True, context={'request': request})
    composition_ser = CompositionSerializer(compositions, many = True, context={'request': request})        
            
    ser_data = {
        'USERS' : user_ser.data,
        'COMPOSITIONS' : composition_ser.data
    }
    return Response(ser_data)    
    
    