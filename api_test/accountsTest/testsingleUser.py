from rest_framework import status
from accounts.models import User
from .base import AccountsTest


class TestSingleUserAPI(AccountsTest):

    """Tests for get/update/delete user API"""

    def test_get_single_account_returns_single_user(self):
        User.objects.create_user('user1@user.com', 'user1')
        url = '/users/1'

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_response = self.getResponseDict(1, 'user1@user.com', 'user1')
        expected_response['IsFollowed'] = False
        self.assertEqual(response.data, expected_response)

    def test_update_returns_forbidden_if_not_logged_in(self):
        User.objects.create_user('user1@user.com', 'user1')
        url = '/users/1'

        response = self.client.put(url, data={'first_name': 'user2'})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_returns_forbidden_if_not_himself(self):
        User.objects.create_user('user1@user.com', 'user1', 'user1')
        User.objects.create_user('user2@user.com', 'user2', 'user2')
        url = '/users/1'

        self.client.login(username='user2@user.com', password='user2')
        response = self.client.put(url, data={'first_name': 'user2'})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_when_user_logged_in_himself(self):
        User.objects.create_user('user1@user.com', 'user1', 'user1')
        url = '/users/1'

        self.client.login(username='user1@user.com', password='user1')
        response = self.client.put(url, data={'first_name': 'user2'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, self.getResponseDict(1, 'user1@user.com', 'user2'))

    def test_delete_throws_forbidden_if_user_not_logged_in(self):
        User.objects.create_user('user1@user.com', 'user1')
        url = '/users/1'

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_throws_forbidden_if_user_not_himself(self):
        User.objects.create_user('user1@user.com', 'user1', 'user1')
        User.objects.create_user('user2@user.com', 'user2', 'user2')
        url = '/users/1'

        self.client.login(username='user2@user.com', password='user2')
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_when_user_himslef(self):
        User.objects.create_user('user1@user.com', 'user1', 'user1')
        url = '/users/1'

        self.client.login(username='user1@user.com', password='user1')
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
