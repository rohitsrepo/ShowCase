from django.shortcuts import render
from myapp.models import Composition
from myapp.serializers import CompositionSerializer
from rest_framework import mixins, generics
from django.contrib.auth.models import User
from myapp.serializers import UserSerializer
from rest_framework import permissions
from myapp.permissions import IsOwnerOrReadOnly
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

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer