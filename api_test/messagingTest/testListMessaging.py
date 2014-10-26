from rest_framework.test import APITestCase
from rest_framework import status
from django.utils.timesince import timesince
from messaging.models import Message
from accounts.models import User
from datetime import datetime


class TestListMessaging(APITestCase):

    """ Tests for send, read and marking messages read."""

    def createResponse(self, id, sender, subject, body, created, read=False):
        time_gap = timesince(created)
        return {'id': id, 'sender': sender, 'body': body, 'subject': subject, 'timesince': time_gap, 'read': read}

    def test_get_returns_forbidden_for_not_authenticated_user(self):
        user = User.objects.create_user('user1@user.com', 'user1', 'user1')
        Message.objects.create(
            sender='user2@user.com', recipient=user, subject='Message', body='This is message.')
        url = '/users/{0}/messages'.format(user.id)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_returns_forbidden_for_authenticated_user_not_himself(self):
        user = User.objects.create_user('user1@user.com', 'user1', 'user1')
        User.objects.create_user('user2@user.com', 'user2', 'user2')
        Message.objects.create(
            sender='user2@user.com', recipient=user, subject='Message', body='This is message.')
        url = '/users/{0}/messages'.format(user.id)

        self.client.login(username='user2@user.com', password='user2')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_returns_all_messages_for_valid_authenticated_user(self):
        user = User.objects.create_user('user1@user.com', 'user1', 'user1')
        User.objects.create_user('user2@user.com', 'user2', 'user2')
        message1 = Message.objects.create(
            sender='user2@user.com', recipient=user, subject='Message1', body='This is message1.')
        message2 = Message.objects.create(
            sender='user3@user.com', recipient=user, subject='Message2', body='This is message2.')
        url = '/users/{0}/messages'.format(user.id)

        self.client.login(username='user1@user.com', password='user1')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data,
                         [self.createResponse(
                             1, 'user2@user.com', 'Message1', 'This is message1.', message1.created),
                          self.createResponse(
                              2, 'user3@user.com', 'Message2', 'This is message2.', message2.created)
                          ])

    def test_post_for_authenticated_sender(self):
        user1 = User.objects.create_user('user1@user.com', 'user1', 'user1')
        user2 = User.objects.create_user('user2@user.com', 'user2', 'user2')
        message_data = {
            "subject": "Message1", "body": "This is message1", "sender": "randomUser@user.com"}
        url = '/users/{0}/messages'.format(user1.id)

        self.client.login(username='user2@user.com', password='user2')
        response = self.client.post(url, message_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, self.createResponse(
            1, user2.email, message_data["subject"], message_data["body"], datetime.now()))
        self.assertEqual(response.data["body"], Message.objects.get(pk=1).body)

    def test_post_for_non_authenticated_sender(self):
        user1 = User.objects.create_user('user1@user.com', 'user1', 'user1')
        User.objects.create_user('user2@user.com', 'user2', 'user2')
        message_data = {
            "subject": "Message1", "body": "This is message1", "sender": "user3@user.com"}
        url = '/users/{0}/messages'.format(user1.id)

        response = self.client.post(url, message_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, self.createResponse(
            1, "user3@user.com", message_data["subject"], message_data["body"], datetime.now()))
        self.assertEqual(response.data["body"], Message.objects.get(pk=1).body)

    def test_post_for_invalid_post_data(self):
        user1 = User.objects.create_user('user1@user.com', 'user1', 'user1')
        User.objects.create_user('user2@user.com', 'user2', 'user2')
        message_data = {
            "subject": "Message1", "body": "This is message1", "sender": "user3@user.com"}
        url = '/users/{0}/messages'.format(user1.id)
        required_fields = ('body', 'subject', 'sender')

        for field in required_fields:
            bad_data = message_data.copy()
            del bad_data[field]

            response = self.client.post(url, bad_data)

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(
                response.data, {field: ['This field is required.']})
            self.assertEqual(Message.objects.all().count(), 0)

    def test_mark_as_read_for_non_authenticated_user(self):
        user = User.objects.create_user('user1@user.com', 'user1', 'user1')
        message1 = Message.objects.create(
            sender='user2@user.com', recipient=user, subject='Message1', body='This is message1.')
        url = '/users/{0}/messages/{1}/mark_as_read'.format(
            user.id, message1.id)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Message.objects.get(pk=1).read, False)

    def test_mark_as_read_for_authenticated_user_not_recipient(self):
        user = User.objects.create_user('user1@user.com', 'user1', 'user1')
        User.objects.create_user('user2@user.com', 'user2', 'user2')
        message1 = Message.objects.create(
            sender='user2@user.com', recipient=user, subject='Message1', body='This is message1.')
        url = '/users/{0}/messages/{1}/mark_as_read'.format(
            user.id, message1.id)

        self.client.login(username="user2@user.com", password="user2")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Message.objects.get(pk=1).read, False)

    def test_mark_as_read_for_auathenticated_valid_recipient(self):
        user = User.objects.create_user('user1@user.com', 'user1', 'user1')
        message1 = Message.objects.create(
            sender='user2@user.com', recipient=user, subject='Message1', body='This is message1.')
        url = '/users/{0}/messages/{1}/mark_as_read'.format(
            user.id, message1.id)

        self.client.login(username=user.email, password="user1")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.createResponse(
            1, "user2@user.com", message1.subject, message1.body, message1.created, True))
        self.assertEqual(Message.objects.get(pk=1).read, True)
