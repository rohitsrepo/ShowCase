import django_filters
from django.db.models import Q
from .models import Composition
from rest_framework import permissions, generics, status
from .serializers import CompositionSerializer
from .permissions import IsOwnerOrReadOnly, IsHimself
from votes import signals
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from accounts.serializers import ExistingUserSerializer
from rest_framework.decorators import api_view, permission_classes
from ShowCase.utils import check_object_permissions


class CompositionFilter(django_filters.FilterSet):
    # TODO - may be default ordering is required around here.
    class Meta:
	model = Composition
	fields = ('artist',)

class CompositionList(APIView):
    ''' Handels listing of compositions and adding new ones.'''
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, format=None):
	compositions = CompositionFilter(request.GET, queryset=Composition.objects.all())
	compositions = compositions.qs
	ser = CompositionSerializer(compositions, many=True)

	if request.user.is_authenticated():
	    counter = 0
	    related_comps = compositions.filter(collectors__id=request.user.id)
	    for composition in compositions:
		ser.data[counter]['IsBookmarked'] = False
		ser.data[counter]['IsVoted'] = False
		
		if composition in related_comps:
		    ser.data[counter]['IsBookmarked'] = True
		if request.user.votes.filter(composition=composition).exists():
		    ser.data[counter]['IsVoted'] = True
		counter = counter + 1
	return Response(ser.data)

    def post(self, request, format=None):
	ser = CompositionSerializer(data=request.DATA, files=request.FILES, context={'request': request})
	if ser.is_valid():
	    ser.object.artist = request.user
	    ser.save()
	    return Response(ser.data, status=status.HTTP_201_CREATED)

	return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class CompositionDetail(APIView):
    '''Handel endpoints for individual composition.'''

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def get_composition(self, pk, request):
	try:
	    composition = Composition.objects.get(pk=pk)
	    check_object_permissions(request, self.permission_classes, composition)
	    return composition 
	except Composition.DoesNotExist:
	    raise Http404

    def get(self, request, pk, format=None):
	composition = self.get_composition(pk, request)
	ser = CompositionSerializer(composition)
	ser.data['IsBookmarked'] = False
	ser.data['IsVoted'] = False
	if(composition.collectors.filter(pk=request.user.id).exists()):
	    ser.data['IsBookmarked'] = True
	if request.user.is_authenticated() and request.user.votes.filter(composition=composition).exists():
	    ser.data['IsVoted'] = True
	    

	return Response(ser.data)

    def put(self, request, pk, format=None):
	composition = self.get_composition(pk, request)
	ser  = CompositionSerializer(composition, data=request.DATA, partial=True)
	if ser.is_valid():
	    ser.save()
	    return Response(ser.data)
	return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
	composition = self.get_composition(pk, request)
	composition.delete()
	return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated, IsHimself))
def follow_compositions(request, format=None):
    # To make it genenric w.r.t. user get user Id in post/get. Then check for permissions.
    check_object_permissions(request, follow_compositions.cls.permission_classes, request.user)
    follows = request.user.follows.all()
    if follows:
	q_object = Q()
	
	for follow in follows:
	    q_object |= Q(artist_id=follow.id)
	
	compositions = Composition.objects.filter(q_object)
	ser = CompositionSerializer(compositions, many=True)
	
	if request.user.is_authenticated():
	    counter = 0
	    related_comps = compositions.filter(collectors__id=request.user.id)  
	    for composition in compositions:
		ser.data[counter]['IsBookmarked'] = False
		ser.data[counter]['IsVoted'] = False
		
		if composition in related_comps:
		    ser.data[counter]['IsBookmarked'] = True
		if request.user.votes.filter(composition=composition).exists():
		    ser.data[counter]['IsVoted'] = True
		counter = counter + 1
	return Response(ser.data)
    return Response([])
