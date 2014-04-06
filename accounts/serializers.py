from rest_framework import serializers
from .models import User
from django.forms import widgets
from django.contrib.auth.hashers import make_password
from django.conf import settings
from ShowCase.serializers import HyperlinkedImageField	      

class NewUserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(max_length=128, widget=widgets.PasswordInput, write_only=True)
    picture = HyperlinkedImageField(source='picture', required=False, 
	     default_url=settings.DEFAULT_USER_PICTURE
	    )

    class Meta:
	model = User
	fields = ('id', 'url', 'email', 'first_name', 'last_name','about', 'password', 'picture')

    def save_object(self, obj, *args, **kwargs):
	#Encrypting password before saving it.
	obj.password = make_password(obj.password)
	super(NewUserSerializer, self).save_object(obj, *args, **kwargs)

class ExistingUserSerializer(serializers.HyperlinkedModelSerializer):
    email = serializers.EmailField(read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='user-detail', lookup_field='pk')
    picture = HyperlinkedImageField(source='picture', required=False, 
	     default_url=settings.DEFAULT_USER_PICTURE
	    )

    class Meta:
	model = User
	fields = ('id', 'url', 'email', 'first_name', 'last_name', 'about', 'picture')

class PasswordUserSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128)
    new_password = serializers.CharField(max_length=128)
    
    def __init__(self, *args, **kwargs):
	super(PasswordUserSerializer, self).__init__(*args, **kwargs)

	try:
	    self.user = self.context['user']
	except KeyError:
	    raise Exception("Please pass user as context instance")    

    def validate_old_password(self, attrs, source):
	'''
	Validate the old password is valid.
	'''

	old_password = attrs[source]
	if self.user.check_password(old_password):
	    return attrs
	else:
	    raise serializers.ValidationError("Old password that you entered is not a valid password")
