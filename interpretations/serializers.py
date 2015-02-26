from rest_framework import serializers
from .models import Interpretation
from accounts.models import User

class InterpretationUserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'full_name')

class InterpretationSerializer(serializers.ModelSerializer):
    user = InterpretationUserSerializer(read_only=True)
    timesince = serializers.CharField(source='timesince', read_only=True)

    class Meta:
        model = Interpretation
        fields = ('id', 'interpretation', 'user', 'composition', 'timesince')
        read_only_fields = ('id', 'composition')
