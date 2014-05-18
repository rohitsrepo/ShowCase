from .models import Composition
from rest_framework import permissions, generics
from .serializers import CompositionSerializer
from .permissions import IsOwnerOrReadOnly
from votes import signals


class CompositionList(generics.ListCreateAPIView):
    queryset = Composition.objects.all()
    serializer_class = CompositionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    
    def pre_save(self, obj):
        obj.artist = self.request.user


class CompositionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Composition.objects.all()
    serializer_class = CompositionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)
    
    def pre_save(self, obj):
        obj.artist = self.request.user
