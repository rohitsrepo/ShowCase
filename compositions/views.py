import django_filters
from .models import Composition
from rest_framework import permissions, generics, status
from .serializers import CompositionSerializer
from .permissions import IsOwnerOrReadOnly
from votes import signals
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404


class CompositionFilter(django_filters.FilterSet):
    # TODO - may be default ordering is required around here.
    class Meta:
	model = Composition
	fields = ('artist',)

class CompositionList(generics.ListCreateAPIView):
    queryset = Composition.objects.all()
    serializer_class = CompositionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_class = CompositionFilter
    
    def pre_save(self, obj):
        obj.artist = self.request.user

class CompositionDetail(APIView):
    '''Handel endpoints for individual composition.'''

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def get_composition(self, pk):
	try:
	    return Composition.objects.get(pk=pk)
	except Composition.DoesNotExist:
	    raise Http404

    def get(self, request, pk, format=None):
	composition = self.get_composition(pk)
	ser = CompositionSerializer(composition)
	ser.data['IsBookmarked'] = False
	ser.data['IsVoted'] = False
	if(composition.user_set.filter(pk=request.user.id).exists()):
	    ser.data['IsBookmarked'] = True
	if request.user.is_authenticated() and request.user.votes.filter(composition=composition).exists():
	    ser.data['IsVoted'] = True
	    

	return Response(ser.data)

    def put(self, request, pk, format=None):
	composition = self.get_composition(pk)
	ser  = CompositionSerializer(composition, data=request.DATA, partial=True)
	if ser.is_valid():
	    ser.save()
	    return Response(ser.data)
	return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
	composition = self.get_serializer(pk)
	composition.delete()
	return Response(status=status.HTTP_204_NO_CONTENT)
