from .base import InterpretationsTest
from interpretations.models import Interpretation
from rest_framework import status
from api_test import Helpers


class TestSingleInterpretation(InterpretationsTest):

    """Tests for updating and deleting interpretation"""

    def test_update_return_forbiddon_for_unauthenticated_user(self):
        user1 = Helpers.getUser(user_data=Helpers.USER1)
        composition = Helpers.getComposition(artist=user1)
        interpretation = Interpretation.objects.create(
            user=user1, composition=composition, interpretation='interpretation1')
        interpretation_data = {'interpretation': 'interpretation2'}
        url = '/compositions/{0}/interpretations/{1}'.format(
            composition.id, interpretation.id)

        response = self.client.put(url, data=interpretation_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_returns_forbidden_for_user_not_interpretationer(self):
        user1 = Helpers.getUser(user_data=Helpers.USER1)
        Helpers.getUser(user_data=Helpers.USER2)
        composition = Helpers.getComposition(artist=user1)
        interpretation = Interpretation.objects.create(
            user=user1, composition=composition, interpretation='interpretation1')
        interpretation_data = {'interpretation': 'interpretation2'}
        url = '/compositions/{0}/interpretations/{1}'.format(
            composition.id, interpretation.id)

        self.client.login(username='user2@user.com', password='user2')
        response = self.client.put(url, data=interpretation_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_for_autheticated_valid_interpretationer(self):
        user1 = Helpers.getUser(user_data=Helpers.USER1)
        Helpers.getUser(user_data=Helpers.USER2)
        composition = Helpers.getComposition(artist=user1)
        interpretation = Interpretation.objects.create(
            user=user1, composition=composition, interpretation='interpretation1')
        interpretation_data = {'interpretation': 'interpretation2'}
        url = '/compositions/{0}/interpretations/{1}'.format(
            composition.id, interpretation.id)

        self.client.login(username='user1@user.com', password='user1')
        response = self.client.put(url, data=interpretation_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.createResponse(
            1, 'interpretation2', user1.id, composition.id, interpretation.created))
        self.assertEqual(Interpretation.objects.all().count(), 1)
        self.assertEqual(Interpretation.objects.get(pk=1).interpretation, interpretation_data["interpretation"])

    def test_delete_return_forbidden_for_non_authenticated_user(self):
        user1 = Helpers.getUser(user_data=Helpers.USER1)
        composition = Helpers.getComposition(artist=user1)
        interpretation = Interpretation.objects.create(
            user=user1, composition=composition, interpretation='interpretation1')
        url = '/compositions/{0}/interpretations/{1}'.format(
            composition.id, interpretation.id)

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_returns_forbidden_for_user_not_interpretationer(self):
        user1 = Helpers.getUser(user_data=Helpers.USER1)
        Helpers.getUser(user_data=Helpers.USER2)
        composition = Helpers.getComposition(artist=user1)
        interpretation = Interpretation.objects.create(
            user=user1, composition=composition, interpretation='interpretation1')
        url = '/compositions/{0}/interpretations/{1}'.format(
            composition.id, interpretation.id)

        self.client.login(username='user2@user.com', password='user2')
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_for_autheticated_valid_interpretationer(self):
        user1 = Helpers.getUser(user_data=Helpers.USER1)
        Helpers.getUser(user_data=Helpers.USER2)
        composition = Helpers.getComposition(artist=user1)
        interpretation = Interpretation.objects.create(
            user=user1, composition=composition, interpretation='interpretation1')
        url = '/compositions/{0}/interpretations/{1}'.format(
            composition.id, interpretation.id)

        self.client.login(username='user1@user.com', password='user1')
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Interpretation.objects.all().count(), 0)
