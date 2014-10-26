from .base import CommentsTest
from compositions.models import Composition
from accounts.models import User
from comments.models import Comment
from rest_framework import status


class TestSingleComment(CommentsTest):

    """Tests for updating and deleting comment"""

    def test_update_return_forbiddon_for_unauthenticated_user(self):
        user1 = User.objects.create_user('user1@user.com', 'user1')
        composition = Composition.objects.create(artist=user1)
        comment = Comment.objects.create(
            commenter=user1, composition=composition, comment='comment1')
        comment_data = {'comment': 'comment2'}
        url = '/compositions/{0}/comments/{1}'.format(
            composition.id, comment.id)

        response = self.client.put(url, data=comment_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_returns_forbidden_for_user_not_commenter(self):
        user1 = User.objects.create_user('user1@user.com', 'user1')
        User.objects.create_user('user2@user.com', 'user2', 'user2')
        composition = Composition.objects.create(artist=user1)
        comment = Comment.objects.create(
            commenter=user1, composition=composition, comment='comment1')
        comment_data = {'comment': 'comment2'}
        url = '/compositions/{0}/comments/{1}'.format(
            composition.id, comment.id)

        self.client.login(username='user2@user.com', password='user2')
        response = self.client.put(url, data=comment_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_for_autheticated_valid_commenter(self):
        user1 = User.objects.create_user('user1@user.com', 'user1', 'user1')
        User.objects.create_user('user2@user.com', 'user2', 'user2')
        composition = Composition.objects.create(artist=user1)
        comment = Comment.objects.create(
            commenter=user1, composition=composition, comment='comment1')
        comment_data = {'comment': 'comment2'}
        url = '/compositions/{0}/comments/{1}'.format(
            composition.id, comment.id)

        self.client.login(username='user1@user.com', password='user1')
        response = self.client.put(url, data=comment_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.createResponse(
            1, 'comment2', user1.id, composition.id, comment.created, True))

    def test_delete_return_forbidden_for_non_authenticated_user(self):
        user1 = User.objects.create_user('user1@user.com', 'user1')
        composition = Composition.objects.create(artist=user1)
        comment = Comment.objects.create(
            commenter=user1, composition=composition, comment='comment1')
        url = '/compositions/{0}/comments/{1}'.format(
            composition.id, comment.id)

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_returns_forbidden_for_user_not_commenter(self):
        user1 = User.objects.create_user('user1@user.com', 'user1')
        User.objects.create_user('user2@user.com', 'user2', 'user2')
        composition = Composition.objects.create(artist=user1)
        comment = Comment.objects.create(
            commenter=user1, composition=composition, comment='comment1')
        url = '/compositions/{0}/comments/{1}'.format(
            composition.id, comment.id)

        self.client.login(username='user2@user.com', password='user2')
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_for_autheticated_valid_commenter(self):
        user1 = User.objects.create_user('user1@user.com', 'user1', 'user1')
        User.objects.create_user('user2@user.com', 'user2', 'user2')
        composition = Composition.objects.create(artist=user1)
        comment = Comment.objects.create(
            commenter=user1, composition=composition, comment='comment1')
        url = '/compositions/{0}/comments/{1}'.format(
            composition.id, comment.id)

        self.client.login(username='user1@user.com', password='user1')
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
