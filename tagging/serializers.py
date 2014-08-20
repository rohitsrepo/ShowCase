from rest_framework import serializers
from .models import Tag
from django.conf import settings

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'tag_name', 'tag_def', 'created')