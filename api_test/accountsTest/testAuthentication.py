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

        response = self.client.post(
            url, data={'email': 'user1@user.com', 'password': 'user1pass'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_response = self.getResponseDict(1, 'user1@user.com', 'user1')
        self.assertEqual(response.data, expected_response)

    def test_login_is_idempotent(self):
        User.objects.create_user('user1@user.com', 'user1', 'user1pass')
        url = '/users/login'

        self.client.post(
            url, data={'email': 'user1@user.com', 'password': 'user1pass'})
        self.client.post(
            url, data={'email': 'user1@user.com', 'password': 'user1pass'})
        response = self.client.post(
            url, data={'email': 'user1@user.com', 'password': 'user1pass'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_response = self.getResponseDict(1, 'user1@user.com', 'user1')
        self.assertEqual(response.data, expected_response)

    def test_login_for_invalid_credentials(self):
        url = '/users/login'

        response = self.client.post(
            url, data={'email': 'user1@user.com', 'password': 'user1pass'})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_for_inactive_account(self):
        user = User.objects.create_user('user1@user.com', 'user1', 'user1pass')
        user.is_active = False
        user.save()
        url = '/users/login'

        response = self.client.post(
            url, data={'email': 'user1@user.com', 'password': 'user1pass'})

        self.assertEqual(
            response.status_code, status.HTTP_402_PAYMENT_REQUIRED)

    def test_reset_password_when_user_not_authenticated(self):
        old_password = "user1"
        new_password = "userNew1"
        user = User.objects.create_user(
            "user1@user.com", "user1", old_password)
        password_data = {
            "old_password": old_password + 'Error', "new_password": new_password}
        url = "/users/{0}/set_password".format(user.id)

        response = self.client.post(url, data=password_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_reset_password_when_user_authenticated_but_not_himself(self):
        old_password = "user1"
        new_password = "userNew1"
        user = User.objects.create_user(
            "user1@user.com", "user1", old_password)
        invalid_user = User.objects.create_user("user2@user.com", "user2", "user2")
        password_data = {
            "old_password": old_password, "new_password": new_password}
        url = "/users/{0}/set_password".format(user.id)

        self.client.login(username=invalid_user.email, password="user2")
        response = self.client.post(url, data=password_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_reset_password_when_old_password_is_wrong(self):
        old_password = "user1"
        new_password = "userNew1"
        user = User.objects.create_user(
            "user1@user.com", "user1", old_password)
        password_data = {
            "old_password": old_password + 'Error', "new_password": new_password}
        url = "/users/{0}/set_password".format(user.id)

        self.client.login(username=user.email, password=old_password)
        response = self.client.post(url, data=password_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reset_password_for_authenticated_valid_user(self):
        old_password = "user1"
        new_password = "userNew1"
        user = User.objects.create_user(
            "user1@user.com", "user1", old_password)
        password_data = {
            "old_password": old_password, "new_password": new_password}
        url = "/users/{0}/set_password".format(user.id)

        self.client.login(username=user.email, password=old_password)
        response = self.client.post(url, data=password_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(
            "/users/login", data={'email': user.email, 'password': new_password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_response = self.getResponseDict(
            1, user.email, user.first_name)
        self.assertEqual(response.data, expected_response)
