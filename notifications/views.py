from rest_framework import status, permissions
from .models import Notification
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from .serializers import NotificationSerializer


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated, ))
def all(request, format=None):
    notifications = request.user.notifications.all()
    ser = NotificationSerializer(notifications, many=True)
    return Response(ser.data)


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated, ))
def unread(request, format=None):
    notifications = request.user.notifications.unread()
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated, ))
def mark_all_as_read(request, format=None):
    request.user.notifications.mark_all_as_read()
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated, ))
def mark_as_read(request, pk, format=None):
    notification = get_object_or_404(Notification, pk=pk)
    notification.mark_as_read()
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated, ))
def check_for_notification(request, format=None):
    result = request.user.notifications.unread().exists()
    return Response({'result': result}, status=status.HTTP_200_OK)
