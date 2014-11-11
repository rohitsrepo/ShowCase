from rest_framework import serializers
from .models import Interpretation


class InterpretationSerializer(serializers.ModelSerializer):
    timesince = serializers.CharField(source='timesince', read_only=True)

    class Meta:
        model = Interpretation
        fields = ('id', 'interpretation', 'user', 'composition', 'timesince')
        read_only_fields = ('id', 'user', 'composition')
