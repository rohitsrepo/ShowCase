from .models import User
from .serializers import NewUserSerializer, ExistingUserSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class UserList(APIView):
    '''
    Creates new user and returns list of existing users.
    '''

    def get(self, request, format=None):
	users = User.objects.all()
	serializer = ExistingUserSerializer(users, many=True)
	return Response(serializer.data)

    def post(self, request, format=None):
	serializer = NewUserSerializer(data=request.DATA)
	if serializer.is_valid():
	    serializer.save()
	    return Response(serializer.data, status=status.HTTP_201_CREATED)
	else:
	    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
