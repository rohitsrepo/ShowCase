from rest_framework import status
from comments.models import Comment
from datetime import datetime
from .base import CommentsTest
from api_test import Helpers


class TestListComments(CommentsTest):

    "Tests for getting list of comments and posting comments"

    def test_get_returns_all_comments_for_interpretation(self):
        user1 = Helpers.getUser(Helpers.USER1)
        user2 = Helpers.getUser(Helpers.USER1)
        interpretation = Helpers.createInterpretation()
        comment1 = Comment.objects.create(
            commenter=user1, interpretation=interpretation, comment='comment1')
        comment2 = Comment.objects.create(
            commenter=user1, interpretation=interpretation, comment='comment2')
        comment3 = Comment.objects.create(
            commenter=user2, interpretation=interpretation, comment='comment3')
        url = '/compositions/{0}/interpretations/{1}/comments'.format(interpretation.composition.id, interpretation.id)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_response = [
            self.createResponse(1, 'comment1', user1.id, interpretation.id, comment1.created)]
        expected_response.append(
            self.createResponse(2, 'comment2', user1.id, interpretation.id, comment2.created))
        expected_response.append(
            self.createResponse(3, 'comment3', user2.id, interpretation.id, comment3.created))
        self.assertEqual(response.data, expected_response)

    def test_get_for_non_existing_interpretation(self):
        Helpers.createComposition()
        url = '/compositions/1/interpretations/1/comments'

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_get_for_non_existing_composition(self):
        url = '/compositions/1/interpretations/1/comments'

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_post_returns_forbidden_for_not_authorized_user(self):
        interpretation = Helpers.createInterpretation()
        url = '/compositions/{0}/interpretations/{1}/comments'.format(interpretation.composition.id, interpretation.id)

        response = self.client.post(url, data={})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data, {"detail": "Authentication credentials were not provided."})
        self.assertEqual(Comment.objects.all().count(), 0)

    def test_post_for_authenticated_user_with_invalid_data(self):
        Helpers.getUser(Helpers.USER2)
        interpretation = Helpers.createInterpretation()
        comment_data = {}
        url = '/compositions/{0}/interpretations/{1}/comments'.format(interpretation.composition.id, interpretation.id)

        self.client.login(username='user2@user.com', password='user2')
        response = self.client.post(url, data=comment_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data, {"comment": ["This field is required."]})
        self.assertEqual(Comment.objects.all().count(), 0)

    def test_post_for_authenticated_user_empty_comment(self):
        Helpers.getUser(Helpers.USER2)
        interpretation = Helpers.createInterpretation()
        comment_data = {'comment': ''}
        url = '/compositions/{0}/interpretations/{1}/comments'.format(interpretation.composition.id, interpretation.id)

        self.client.login(username='user2@user.com', password='user2')
        response = self.client.post(url, data=comment_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data, {"comment": ["This field is required."]})
        self.assertEqual(Comment.objects.all().count(), 0)

    def test_post_authenticated_user_valid_post_data(self):
        user2 = Helpers.getUser(Helpers.USER2)
        interpretation = Helpers.createInterpretation()
        comment_data = {'comment': 'comment1'}
        url = '/compositions/{0}/interpretations/{1}/comments'.format(interpretation.composition.id, interpretation.id)

        self.client.login(username='user2@user.com', password='user2')
        response = self.client.post(url, data=comment_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, self.createResponse(
            1, 'comment1', user2.id, interpretation.id, datetime.now()))
        self.assertEqual(Comment.objects.all().count(), 1)
