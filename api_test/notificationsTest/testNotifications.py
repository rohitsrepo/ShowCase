from rest_framework.test import APITestCase
from rest_framework import status
from api_test import Helpers
from notifications import notify
from django.utils.timesince import timesince
from datetime import datetime
from notifications.models import Notification
from uuid import uuid4


class TestNotifications(APITestCase):

    """ Tests for notifications API. """
    url = "/notifications"
    maxDiff = None

    def createNotification(self, verb=None):
        if not verb:
            verb = "did something"
        user1 = Helpers.getUser(Helpers.USER1)
        user2 = Helpers.getUser(Helpers.USER2)

        comment = Helpers.createComment()
        action_object = comment
        target_object = comment.interpretation

        notification_data = {"actor": user1,
                             "recipient": user2,
                             "verb": verb,
                             "action_object": action_object,
                             "target": target_object}

        notify.send(user1, **notification_data)

        return notification_data

    def createResponse(self,
                       id,
                       recipient_id,
                       verb,
                       created,
                       actor,
                       action_object,
                       target,
                       unread=True):
        time_gap = timesince(created)
        return {"id": id,
                "recipient": recipient_id,
                "unread": unread,
                "verb": verb,
                "timesince": time_gap,
                "actor": self.createReponseInnerObjects(actor),
                "target": self.createReponseInnerObjects(target),
                "action_object": self.createReponseInnerObjects(action_object)}

    def createReponseInnerObjects(self, inner_object):
        if not inner_object:
            return {}
        return {"obj": unicode(inner_object), "url": inner_object.get_absolute_url()}

    def test_all_returns_all_notifications(self):
        notification1_data = self.createNotification()
        notification2_data = self.createNotification()
        user = Helpers.getUser(Helpers.USER2)

        self.client.login(
            username=user.email, password=Helpers.USER2["password"])
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_response = [self.createResponse(2,
                                                 user.id,
                                                 notification2_data["verb"],
                                                 datetime.now(),
                                                 notification2_data["actor"],
                                                 notification2_data[
                                                     "action_object"],
                                                 notification2_data["target"])]
        expected_response += [self.createResponse(1,
                                                  user.id,
                                                  notification1_data["verb"],
                                                  datetime.now(),
                                                  notification1_data["actor"],
                                                  notification1_data[
                                                      "action_object"],
                                                  notification1_data["target"])]
        self.assertEqual(response.data, expected_response)

    def test_all_returns_forbidden_for_non_authenticated_user(self):
        self.createNotification()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unread_returns_unread_notifications(self):
        notification1_data = self.createNotification("Action1")
        self.createNotification("Action2")
        notification3_data = self.createNotification("Action3")
        notification = Notification.objects.get(pk=2)
        notification.unread = False
        notification.save()
        user = Helpers.getUser(Helpers.USER2)
        url = self.url + "/unread"

        self.client.login(
            username=user.email, password=Helpers.USER2["password"])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_response = [self.createResponse(3,
                                                 user.id,
                                                 notification3_data["verb"],
                                                 datetime.now(),
                                                 notification3_data["actor"],
                                                 notification3_data[
                                                     "action_object"],
                                                 notification3_data["target"])]
        expected_response += [self.createResponse(1,
                                                  user.id,
                                                  notification1_data["verb"],
                                                  datetime.now(),
                                                  notification1_data["actor"],
                                                  notification1_data[
                                                      "action_object"],
                                                  notification1_data["target"])]
        self.assertEqual(response.data, expected_response)

    def test_unread_returns_forbidden_for_non_authenticated_user(self):
        self.createNotification()
        url = self.url + "/unread"

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_mark_all_marks_all_notifications_read(self):
        self.createNotification()
        self.createNotification()
        self.createNotification()
        user = Helpers.getUser(Helpers.USER2)
        url = self.url + "/mark-all-as-read"

        self.client.login(
            username=user.email, password=Helpers.USER2["password"])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Notification.objects.filter(unread=True).count(), 0)

    def test_mark_all_returns_forbidden_for_non_authenticated_user(self):
        self.createNotification()
        url = self.url + "/mark-all-as-read"

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_mark_all_is_idempotent(self):
        self.createNotification()
        self.createNotification()
        self.createNotification()
        user = Helpers.getUser(Helpers.USER2)
        url = self.url + "/mark-all-as-read"

        self.client.login(
            username=user.email, password=Helpers.USER2["password"])
        self.client.get(url)
        self.client.get(url)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Notification.objects.filter(unread=True).count(), 0)

    def test_mark_as_read_marks_a_notification_read(self):
        self.createNotification()
        custom_action = str(uuid4())
        self.createNotification(custom_action)
        self.createNotification()
        user = Helpers.getUser(Helpers.USER2)
        notification_object = Notification.objects.get(
            verb__exact=custom_action)
        url = self.url + "/{0}/mark-as-read".format(notification_object.id)

        self.assertEqual(notification_object.unread, True)

        self.client.login(
            username=user.email, password=Helpers.USER2["password"])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Notification.objects.get(verb__exact=custom_action).unread, False)
        self.assertEqual(Notification.objects.filter(unread=True).count(), 2)

    def test_mark_as_read_returns_forbidden_for_non_authenticated_user(self):
        self.createNotification()
        url = self.url + "/1/mark-as-read"

        response = self.client.get(url)

        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN)

    def test_mark_as_read_is_idempotent(self):
        self.createNotification()
        custom_action = str(uuid4())
        self.createNotification(custom_action)
        self.createNotification()
        user = Helpers.getUser(Helpers.USER2)
        notification_object = Notification.objects.get(
            verb__exact=custom_action)
        url = self.url + "/{0}/mark-as-read".format(notification_object.id)

        self.assertEqual(notification_object.unread, True)

        self.client.login(
            username=user.email, password=Helpers.USER2["password"])
        self.client.get(url)
        self.client.get(url)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Notification.objects.get(verb__exact=custom_action).unread, False)
        self.assertEqual(Notification.objects.filter(unread=True).count(), 2)

    def test_check_for_notifications_returns_true_if_unread_notifications_present(self):
        self.createNotification()
        user = Helpers.getUser(Helpers.USER2)
        url = self.url + "/check"

        self.client.login(
            username=user.email, password=Helpers.USER2["password"])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'result': True})

    def test_check_for_notifications_returns_false_if_no_unread_notification_present(self):
        custom_action = str(uuid4())
        self.createNotification(custom_action)
        notification_object = Notification.objects.get(
            verb__exact=custom_action)
        notification_object.unread = False
        notification_object.save()
        user = Helpers.getUser(Helpers.USER2)
        url = self.url + "/check"

        self.client.login(
            username=user.email, password=Helpers.USER2["password"])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'result': False})

    def test_check_for_notifications_returns_forbidden_for_non_authenticated_user(self):
        self.createNotification()
        url = self.url + "/check"

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_check_for_notifications_call_is_idempotent(self):
        self.createNotification()
        user = Helpers.getUser(Helpers.USER2)
        url = self.url + "/check"

        self.client.login(
            username=user.email, password=Helpers.USER2["password"])
        self.client.get(url)
        self.client.get(url)
        self.client.get(url)
        self.client.get(url)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'result': True})