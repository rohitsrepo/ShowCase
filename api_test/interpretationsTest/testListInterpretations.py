from rest_framework import status
from interpretations.models import Interpretation
from datetime import datetime
from .base import InterpretationsTest
from api_test import Helpers


class TestListInterpretations(InterpretationsTest):

    "Tests for getting list of interpretations and posting interpretations"

    def test_get_returns_all_interpretations_for_composition(self):
        user1 = Helpers.getUser(user_data=Helpers.USER1)
        user2 = Helpers.getUser(user_data=Helpers.USER2)
        composition = Helpers.getComposition(artist=user1)
        interpretation1 = Interpretation.objects.create(
            user=user1, composition=composition, interpretation='interpretation1')
        interpretation2 = Interpretation.objects.create(
            user=user1, composition=composition, interpretation='interpretation2')
        interpretation3 = Interpretation.objects.create(
            user=user2, composition=composition, interpretation='interpretation3')
        url = '/compositions/{0}/interpretations'.format(composition.id)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_response = [
            self.createResponse(1, 'interpretation1', user1.id, composition.id, interpretation1.created)]
        expected_response.append(
            self.createResponse(2, 'interpretation2', user1.id, composition.id, interpretation2.created))
        expected_response.append(
            self.createResponse(3, 'interpretation3', user2.id, composition.id, interpretation3.created))
        self.assertEqual(response.data, expected_response)

    def test_get_for_non_existing_composition(self):
        url = '/compositions/1/interpretations'

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_post_returns_forbidden_for_not_authorized_user(self):
        user1 = Helpers.getUser(user_data=Helpers.USER1)
        composition = Helpers.getComposition(artist=user1)
        url = '/compositions/{0}/interpretations'.format(composition.id)

        response = self.client.post(url, data={})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data, {"detail": "Authentication credentials were not provided."})

    def test_post_for_authenticated_user_with_invalid_data(self):
        user1 = Helpers.getUser(user_data=Helpers.USER1)
        Helpers.getUser(user_data=Helpers.USER2)
        composition = Helpers.getComposition(artist=user1)
        interpretation_data = {}
        url = '/compositions/{0}/interpretations'.format(composition.id)

        self.client.login(username='user2@user.com', password='user2')
        response = self.client.post(url, data=interpretation_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data, {"interpretation": ["This field is required."]})

    def test_post_for_authenticated_user_empty_interpretation(self):
        user1 = Helpers.getUser(user_data=Helpers.USER1)
        Helpers.getUser(user_data=Helpers.USER2)
        composition = Helpers.getComposition(artist=user1)
        interpretation_data = {'interpretation': ''}
        url = '/compositions/{0}/interpretations'.format(composition.id)

        self.client.login(username='user2@user.com', password='user2')
        response = self.client.post(url, data=interpretation_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data, {"interpretation": ["This field is required."]})

    def test_post_authenticated_user_valid_post_data(self):
        user1 = Helpers.getUser(user_data=Helpers.USER1)
        user2 = Helpers.getUser(user_data=Helpers.USER2)
        composition = Helpers.getComposition(artist=user1)
        interpretation_data = {'interpretation': 'interpretation1'}
        url = '/compositions/{0}/interpretations'.format(composition.id)

        self.client.login(username='user2@user.com', password='user2')
        response = self.client.post(url, data=interpretation_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, self.createResponse(
            1, 'interpretation1', user2.id, composition.id, datetime.now()))
        self.assertEqual(Interpretation.objects.get(pk=1).interpretation, interpretation_data["interpretation"])
        self.assertEqual(Interpretation.objects.all().count(), 1)
