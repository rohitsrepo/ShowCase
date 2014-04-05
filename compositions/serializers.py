from django.forms import widgets
from rest_framework import serializers
from myapp.models import Composition
from django.contrib.auth.models import User


class CompositionSerializer(serializers.ModelSerializer):
    artist = serializers.Field(source='artist.username')
    class Meta:
        model = Composition
        fields = ('id', 'title', 'artist', 'description')
    
class UserSerializer(serializers.ModelSerializer):
    compositions = serializers.PrimaryKeyRelatedField(many=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'compositions')

