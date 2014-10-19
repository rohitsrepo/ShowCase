import os
from rest_framework import status
from accounts.models import User
from .base import AccountsTest


class TestAccountsAPI(AccountsTest):

    """Tests for get list of users and Add new user API"""

    def test_list_accounts_returns_all_users(self):
        User.objects.create_user('abc@def.com', 'abc')
        User.objects.create_user('abc1@def.com', 'abc1')
        url = '/users'

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0],
                         self.getResponseDict(1, 'abc@def.com', 'abc'))
        self.assertEqual(
            response.data[1],
            self.getResponseDict(2, 'abc1@def.com', 'abc1'))

    def test_add_user_returns_valid_response(self):
        with open(os.path.join(os.path.dirname(__file__), 'test.JPG')) as account_picture:
            user_data = {'email': 'abc@def.com',
                         'first_name': 'abc',
                         'password': 'abc',
                         'last_name': 'def',
                         'about': 'xyz',
                         'picture': account_picture}
            url = '/users'

            response = self.client.post(url, data=user_data)

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            saved_profile_image = 'Users/{0}/Profile/test.JPG'.format('abc')
            self.assertEqual(
                response.data,
                self.getResponseDict(
                    1, 'abc@def.com', 'abc', saved_profile_image, 'def', 'xyz'
                )
            )

    def test_add_default_picture_is_added_if_no_picture_sent(self):
        user_data = {'email': 'abc@def.com', 'first_name': 'abc',
                     'password': 'abc', 'last_name': '', 'about': ''}
        url = '/users'

        response = self.client.post(url, data=user_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data, self.getResponseDict(1, 'abc@def.com', 'abc'))

    def test_valid_error_response_on_invalid_data_missing_required_fields(self):
        user_data = {'email': 'abc@def.com',
                     'first_name': 'abc',
                     'password': 'abc',
                     'last_name': '',
                     'about': '',
                     'picture': ''}
        required_fields = ('email', 'first_name', 'password')
        url = '/users'

        for field in required_fields:
            bad_data_holder = user_data.copy()
            del bad_data_holder[field]

            response = self.client.post(url, data=bad_data_holder)

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            expected_response_error = {field: ['This field is required.']}
            self.assertEqual(response.data, expected_response_error)
