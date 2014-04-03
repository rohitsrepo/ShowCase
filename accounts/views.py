from .models import User
from .serializers import NewUserSerializer, ExistingUserSerializer, PasswordUserSerializer
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework import generics

class UserList(generics.ListCreateAPIView):
    '''
    Creates and lists users.
    '''
    queryset = User.objects.all()
    serializer_class = NewUserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    '''
    Retrieves, updates and deletes a particular user.
    '''
    queryset = User.objects.all()
    serializer_class = ExistingUserSerializer

@api_view(['POST'])
def reset_password(request, pk, format=None):
    '''
    Changes user password.

    Offloading validation like both values entered in new password fields are same, to frontend.
    '''
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        raise Http404

    serializer = PasswordUserSerializer(request.DATA, data=request.DATA,context={'user':user})
    if serializer.is_valid():
	user.set_password(serializer.data['new_password'])
	user.save()
	return Response()
    else:
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

