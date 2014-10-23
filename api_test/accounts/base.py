from rest_framework.test import APITestCase


class AccountsTest(APITestCase):

    """Tests for accounts API"""

    def setUp(self):
        self.default_user_picture = '/media/root/user_default.jpg'

    def getResponseDict(self,
                        id,
                        email,
                        first_name,
                        picture='',
                        last_name='',
                        about=''):

        if not picture:
            picture = self.default_user_picture
        return {'id':  id,
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'about': about,
                'picture': picture}
