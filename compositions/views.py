from django.shortcuts import render
from .models import Composition
from rest_framework import mixins, generics
from .serializers import CompositionSerializer
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly
# Create your views here.

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
