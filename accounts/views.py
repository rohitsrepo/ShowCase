from .models import User
from .serializers import NewUserSerializer, ExistingUserSerializer, PasswordUserSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

def get_object(pk):
    try:
        return User.objects.get(pk=pk)
    except User.DoesNotExist:
        raise Http404


class UserList(APIView):
    '''
    Creates new user and returns list of existing users.
    '''

    def get(self, request, format=None):
	users = User.objects.all()
	serializer = NewUserSerializer(users, many=True, context={'request': request})
	return Response(serializer.data)

    def post(self, request, format=None):
	serializer = NewUserSerializer(data=request.DATA, context={'request':request})
	if serializer.is_valid():
	    serializer.save()
	    return Response(serializer.data, status=status.HTTP_201_CREATED)
	else:
	    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetail(APIView):
    '''
    Retrieves, updates and deletes a particular user.
    '''

   
    def get(self, request, pk, format=None):
	user = get_object(pk)
	serializer = ExistingUserSerializer(user, context={'request':request})
	return Response(serializer.data)

    def put(self, request, pk, format=None):
	user = get_object(pk)
	serializer = ExistingUserSerializer(user, data=request.DATA, context={'request':request})
	if serializer.is_valid():
	    serializer.save()
	    return Response(serializer.data)
	else:
	    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
	user = get_object(pk)
	user.delete()
	return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def reset_password(request, pk, format=None):
    '''
    Changes user password.

    Offloading validation like both values entered in new password fields are same, to frontend.
    '''

    user = get_object(pk)
    serializer = PasswordUserSerializer(request.DATA, data=request.DATA,context={'user':user})
    if serializer.is_valid():
	user.set_password(serializer.data['new_password'])
	user.save()
	return Response()
    else:
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

