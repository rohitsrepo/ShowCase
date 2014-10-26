import os, shutil
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import User
from django.conf import settings

class TestAccountsAPI(APITestCase):
	"""Tests for accounts API"""
	def setUp(self):
		self.default_user_picture = '/media/root/user_default.jpg'

	def tearDown(self):
		media_dir = settings.MEDIA_ROOT
		shutil.rmtree(media_dir, True)

	def test_list_accounts_returns_all_users(self):
		first_user = User.objects.create_user('abc@def.com', 'abc')
		second_user = User.objects.create_user('abc1@def.com', 'abc1')
		url = '/users'

		response = self.client.get(url)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data), 2)
		self.assertEqual(response.data[0], {'id': 1, 'email': 'abc@def.com', 'first_name': 'abc', 'last_name': '', 'about': '', 'picture': self.default_user_picture})
		self.assertEqual(response.data[1], {'id': 2, 'email': 'abc1@def.com', 'first_name': 'abc1', 'last_name': '', 'about': '', 'picture': self.default_user_picture})

	def test_add_user_returns_valid_response(self):
		with open(os.path.join(os.path.dirname(__file__), 'test.JPG')) as account_picture:
			user_data = {'email': 'abc@def.com', 'first_name': 'abc', 'password': 'abc', 'last_name': '', 'about': '', 'picture': account_picture}
			url = '/users'

			response = self.client.post(url, data=user_data)

			self.assertEqual(response.status_code, status.HTTP_201_CREATED)
			saved_profile_picture = 'Users/{0}/Profile/test.JPG'.format('abc')
			self.assertEqual(response.data, {'id': 1, 'email': 'abc@def.com', 'first_name': 'abc', 'last_name': '', 'about': '', 'picture': saved_profile_picture})


	def test_add_default_picture_is_added_if_no_picture_sent(self):
		user_data = {'email': 'abc@def.com', 'first_name': 'abc','password': 'abc', 'last_name': '', 'about': ''}
		url = '/users'

		response = self.client.post(url, data=user_data)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response.data, {'id': 1, 'email': 'abc@def.com', 'first_name': 'abc', 'last_name': '', 'about': '', 'picture': self.default_user_picture})

	def test_valid_error_response_on_invalid_data_missing_required_fields(self):
		user_data = {'email': 'abc@def.com', 'first_name': 'abc','password': 'abc', 'last_name': '', 'about': '', 'picture': ''}
		required_fields = ('email', 'first_name', 'password')
		url = '/users'

		for field in required_fields:
			bad_data_holder = user_data.copy()
			del bad_data_holder[field]

			response = self.client.post(url, data=bad_data_holder)
			
			self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
			expected_response_error = {field: ['This field is required.']}
			self.assertEqual(response.data, expected_response_error)

	def test_get_single_account_returns_single_user(self):
		first_user = User.objects.create_user('abc@def.com', 'abc')
		url = '/users/1'

		response = self.client.get(url)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data, {'id': 1, 'email': 'abc@def.com', 'first_name': 'abc', 'last_name': '', 'about': '', 'picture': self.default_user_picture, 'IsFollowed': False})

	def test_update_returns_forbidden_if_not_logged_in(self):
		first_user = User.objects.create_user('abc@def.com', 'abc')
		url = '/users/1'

		response = self.client.put(url, data={'first_name': 'abc1'})

		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

	def test_update_returns_forbidden_if_not_himself(self):
		first_user = User.objects.create_user('abc@def.com', 'abc', 'abc')
		second_user = User.objects.create_user('abc1@def.com', 'abc1', 'abc1')
		url = '/users/1'

		self.client.login(username='abc1@def.com', password='abc1')
		response = self.client.put(url, data={'first_name': 'abc1'})

		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

	def test_update_when_user_logged_in_himself(self):
		first_user = User.objects.create_user('abc@def.com', 'abc', 'abc')
		url = '/users/1'

		self.client.login(username='abc@def.com', password='abc')
		response = self.client.put(url, data={'first_name': 'abc1'})

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data, {'id': 1, 'email': 'abc@def.com', 'first_name': 'abc1', 'last_name': '', 'about': '', 'picture': self.default_user_picture})

	def test_delete_throws_forbidden_if_user_not_logged_in(self):
		first_user = User.objects.create_user('abc@def.com', 'abc')
		url = '/users/1'

		response = self.client.delete(url)

		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

	def test_delete_throws_forbidden_if_user_not_himself(self):
		first_user = User.objects.create_user('abc@def.com', 'abc', 'abc')
		second_user = User.objects.create_user('abc1@def.com', 'abc1', 'abc1')
		url = '/users/1'
		
		self.client.login(username='abc1@def.com', password='abc1')
		response = self.client.delete(url)

		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

	def test_delete_when_user_himslef(self):
		first_user = User.objects.create_user('abc@def.com', 'abc', 'abc')
		url = '/users/1'
		
		self.client.login(username='abc@def.com', password='abc')
		response = self.client.delete(url)

		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)