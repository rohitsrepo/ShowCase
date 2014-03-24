from rest_framework import serializers
from accounts.models import User
from django.forms import widgets
from django.contrib.auth.hashers import make_password

class NewUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, widget=widgets.PasswordInput, write_only=True)

    class Meta:
	model = User
	fields = ('id','email', 'first_name', 'last_name','about', 'password')

    def save_object(self, obj):
	#Encrypting password before saving it.
	obj.password = make_password(obj.password)
	super(NewUserSerializer, self).save_object(obj)

class ExistingUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)

    class Meta:
	model = User
	fields = ('id', 'email', 'first_name', 'last_name', 'about')

class PasswordUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, widget=widgets.PasswordInput)
    new_password = serializers.CharField(max_length=128, widget=widgets.PasswordInput)

    class Meta:
	model = User
	fields = ('password')
