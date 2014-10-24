import smtplib
from .models import Message
from .serializers import MessageSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from accounts.models import User
from .permissions import AuthenticatedGetOrPostOnly
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError


def mailsender():
    account = settings.SHOWCASE_ACCOUNT
    password = settings.SHOWCASE_PASSWORD
    messages = Message.objects.filter(read=False)
    for message in messages:
        sender_name = settings.MAIL_SENDER
        recipient_name = User.objects.get(
            email=message.recipient.get_email()).get_full_name()
        sender_email = message.sender
        recipient_email = message.recipient.get_email()
        subject = message.subject
        body = message.body
        emailText = "From: " + sender_name + " <" + sender_email + ">\nTo: " + recipient_name + \
            " <" + recipient_email + ">\nSubject: " + \
            subject + "\n\n" + body + "\n"
        try:
            smtpObj = smtplib.SMTP('smtp.gmail.com', 587)  # or 465
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.login(account, password)
            smtpObj.sendmail(sender_email, recipient_email, emailText)
            message.read = True
            print "Successfully sent email of Object id: " + message.id + "\n"
        except:
            print "Error: unable to send email of Object id: " + message.id + "\n"
        finally:
            smtpObj.close()


class MessageList(APIView):
    permission_classes = (AuthenticatedGetOrPostOnly, )

    def get(self, request, pk, format=None):
        messages = Message.objects.filter(recipient=request.user)
        serializer = MessageSerializer(
            messages, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        serializer = MessageSerializer(
            data=request.DATA, context={'request': request})

        try:
            if request.user.is_authenticated():
                sender_email = request.user.email
            else:
                sender_email = request.DATA['sender']
        except MultiValueDictKeyError:
            return Response({'sender': ['This field is required.']}, status=status.HTTP_400_BAD_REQUEST)

        recipient = User.objects.get(pk=pk)
        if serializer.is_valid():
            serializer.object.sender = sender_email
            serializer.object.recipient = recipient
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((AuthenticatedGetOrPostOnly,))
def markAsRead(request, pk, message_id, format=None):
    message = get_object_or_404(Message, pk=message_id)
    message.read = True
    message.save()

    serializer = MessageSerializer(message, context={'request': request})

    return Response(serializer.data, status=status.HTTP_200_OK)
