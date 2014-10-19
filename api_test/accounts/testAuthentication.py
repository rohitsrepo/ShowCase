from rest_framework import status
from accounts.models import User
from .base import AccountsTest


class TestAuthenticationAPI(AccountsTest):

    """Tests for user authentication."""

    def test_current_user_when_user_not_logged_in(self):
        url = '/users/currentUser'

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_current_user_for_looged_in_user(self):
        User.objects.create_user('user1@user.com', 'user1', 'user1pass')
        url = '/users/currentUser'

        self.client.login(username='user1@user.com', password='user1pass')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_response = self.getResponseDict(1, 'user1@user.com', 'user1')
        self.assertEqual(response.data, expected_response)

    def test_logout(self):
        User.objects.create_user('user1@user.com', 'user1', 'user1pass')
        url = '/users/logout'
        self.client.login(username='user1@user.com', password='user1pass')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/users/currentUser')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_is_idempotent(self):
        User.objects.create_user('user1@user.com', 'user1', 'user1pass')
        url = '/users/logout'
        self.client.login(username='user1@user.com', password='user1pass')

        self.client.get(url)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_for_valid_credentials(self):
        User.objects.create_user('user1@user.com', 'user1', 'user1pass')
        url = '/users/login'

        response = self.client.post(url, data={'email':'user1@user.com', 'password':'user1pass'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_response = self.getResponseDict(1, 'user1@user.com', 'user1')
        self.assertEqual(response.data, expected_response)

    def test_login_for_invalid_credentials(self):
        url = '/users/login'

        response = self.client.post(url, data={'email':'user1@user.com', 'password':'user1pass'})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_for_inactive_account(self):
        user = User.objects.create_user('user1@user.com', 'user1', 'user1pass')
        user.is_active = False
        user.save()
        url = '/users/login'

        response = self.client.post(url, data={'email':'user1@user.com', 'password':'user1pass'})

        self.assertEqual(
            response.status_code, status.HTTP_402_PAYMENT_REQUIRED)
