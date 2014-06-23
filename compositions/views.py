import django_filters
from .models import Composition
from rest_framework import permissions, generics
from .serializers import CompositionSerializer
from .permissions import IsOwnerOrReadOnly
from votes import signals


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


class CompositionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Composition.objects.all()
    serializer_class = CompositionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)
    
    def pre_save(self, obj):
        obj.artist = self.request.user

    def get_serializer(self, *args, **kwargs):
	kwargs['partial'] = True
	return super(CompositionDetail, self).get_serializer(*args, **kwargs);
