from rest_framework import status
from .base import AccountsTest
from api_test import Helpers


class TestBookmarks(AccountsTest):

    """ Tests for user bookmarking API"""
    url = "/users/{0}/bookmarks"

    def createReponseBookmark(self,
                              id,
                              artist,
                              created,
                              matter='',
                              title='',
                              description='',
                              slug=''):
        return {'id': id,
                'title': title,
                'description': description,
                'artist': artist,
                'slug': slug,
                'created': created,
                'matter': matter}

    def test_get_throws_forbidden_when_user_not_authenticated(self):
        user = Helpers.getUser(Helpers.USER1)
        composition1 = Helpers.createComposition(user)
        composition2 = Helpers.createComposition(user)
        user.bookmarks.add(composition1, composition2)
        url = self.url.format(user.id)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_throws_forbidden_when_user_not_himself(self):
        user = Helpers.getUser(Helpers.USER1)
        other_user = Helpers.getUser(Helpers.USER2)
        composition1 = Helpers.createComposition(user)
        composition2 = Helpers.createComposition(user)
        user.bookmarks.add(composition1, composition2)
        url = self.url.format(user.id)

        self.client.login(
            username=other_user.email, password=Helpers.USER2["password"])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_returns_all_user_bookmarks(self):
        user = Helpers.getUser(Helpers.USER1)
        composition1 = Helpers.createComposition(user)
        composition2 = Helpers.createComposition(user)
        user.bookmarks.add(composition1, composition2)
        url = self.url.format(user.id)

        self.client.login(
            username=user.email, password=Helpers.USER1["password"])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_response = [
            self.createReponseBookmark(1, user.id, composition1.created)]
        expected_response.append(
            self.createReponseBookmark(2, user.id, composition2.created))
        self.assertEqual(response.data, {'bookmarks': expected_response})

    def test_post_throws_forbidden_for_not_authenticated_user(self):
        user = Helpers.getUser(Helpers.USER1)
        composition = Helpers.createComposition(user)
        bookmark_data = {'bookmarks': [composition.id]}
        url = self.url.format(user.id)

        response = self.client.post(url, bookmark_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(user.bookmarks.all().count(), 0)

    def test_post_throws_forbidden_for_authenticated_user_not_himself(self):
        user = Helpers.getUser(Helpers.USER1)
        other_user = Helpers.getUser(Helpers.USER2)
        composition = Helpers.createComposition(user)
        bookmark_data = {'bookmarks': [composition.id]}
        url = self.url.format(user.id)

        self.client.login(
            username=other_user.email, password=Helpers.USER2["password"])
        response = self.client.post(url, bookmark_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(user.bookmarks.all().count(), 0)

    def test_post_throws_400_for_invalid_post_data(self):
        user = Helpers.getUser(Helpers.USER1)
        composition = Helpers.createComposition(user)
        url = self.url.format(user.id)

        self.client.login(
            username=user.email, password=Helpers.USER1["password"])
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data, {"bookmarks": "This field is required"})
        self.assertEqual(user.bookmarks.all().count(), 0)

    def test_post_adds_bookmark_for_valid_authenticated_user(self):
        user = Helpers.getUser(Helpers.USER1)
        composition = Helpers.createComposition(user)
        bookmark_data = {'bookmarks': [composition.id]}
        url = self.url.format(user.id)

        self.client.login(
            username=user.email, password=Helpers.USER1["password"])
        response = self.client.post(url, bookmark_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user.bookmarks.all().count(), 1)

    def test_post_for_already_added_bookmark_acts_same_as_adding_new(self):
        user = Helpers.getUser(Helpers.USER1)
        composition = Helpers.createComposition(user)
        user.bookmarks.add(composition)
        bookmark_data = {'bookmarks': [composition.id]}
        url = self.url.format(user.id)

        self.client.login(
            username=user.email, password=Helpers.USER1["password"])
        response = self.client.post(url, bookmark_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user.bookmarks.all().count(), 1)

    def test_post_works_with_multiple_bookmarks_all_new(self):
        user = Helpers.getUser(Helpers.USER1)
        composition1 = Helpers.createComposition(user)
        composition2 = Helpers.createComposition(user)
        composition3 = Helpers.createComposition(user)
        bookmark_data = {
            'bookmarks': [composition1.id, composition2.id, composition3.id]}
        url = self.url.format(user.id)

        self.client.login(
            username=user.email, password=Helpers.USER1["password"])
        response = self.client.post(url, data=bookmark_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user.bookmarks.all().count(), 3)

    def test_post_works_with_multiple_bookmarks_some_already_exist(self):
        user = Helpers.getUser(Helpers.USER1)
        composition1 = Helpers.createComposition(user)
        composition2 = Helpers.createComposition(user)
        composition3 = Helpers.createComposition(user)
        user.bookmarks.add(composition3)
        bookmark_data = {'bookmarks': [composition1.id, composition2.id]}
        url = self.url.format(user.id)

        self.client.login(
            username=user.email, password=Helpers.USER1["password"])
        response = self.client.post(url, data=bookmark_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user.bookmarks.all().count(), 3)

    def test_delete_throws_forbidden_for_not_authenticated_user(self):
        user = Helpers.getUser(Helpers.USER1)
        composition1 = Helpers.createComposition(user)
        composition2 = Helpers.createComposition(user)
        user.bookmarks.add(composition1, composition2)
        bookmark_data = {'bookmarks': [composition2.id]}
        url = self.url.format(user.id)

        response = self.client.delete(url, data=bookmark_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(user.bookmarks.all().count(), 2)

    def test_delete_throws_forbidden_for_authenticated_user_not_himself(self):
        user = Helpers.getUser(Helpers.USER1)
        other_user = Helpers.getUser(Helpers.USER2)
        composition1 = Helpers.createComposition(user)
        composition2 = Helpers.createComposition(user)
        user.bookmarks.add(composition1, composition2)
        bookmark_data = {'bookmarks': [composition2.id]}
        url = self.url.format(user.id)

        self.client.login(
            username=other_user.email, password=Helpers.USER2["password"])
        response = self.client.delete(url, data=bookmark_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(user.bookmarks.all().count(), 2)

    def test_delete_throws_400_for_invalid_data(self):
        user = Helpers.getUser(Helpers.USER1)
        composition1 = Helpers.createComposition(user)
        composition2 = Helpers.createComposition(user)
        user.bookmarks.add(composition1, composition2)
        url = self.url.format(user.id)

        self.client.login(
            username=user.email, password=Helpers.USER1["password"])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data, {"bookmarks": "This field is required"})
        self.assertEqual(user.bookmarks.all().count(), 2)

    def test_delete_removes_bookmark_for_valid_authenticated_user(self):
        user = Helpers.getUser(Helpers.USER1)
        composition1 = Helpers.createComposition(user)
        composition2 = Helpers.createComposition(user)
        user.bookmarks.add(composition1, composition2)
        bookmark_data = {'bookmarks': [composition2.id]}
        url = self.url.format(user.id)

        self.client.login(
            username=user.email, password=Helpers.USER1["password"])
        response = self.client.delete(url, data=bookmark_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user.bookmarks.all().count(), 1)

    def test_delete_for_non_existing_bookmark_does_not_crash(self):
        user = Helpers.getUser(Helpers.USER1)
        composition1 = Helpers.createComposition(user)
        user.bookmarks.add(composition1)
        bookmark_data = {'bookmarks': [56, 89]}
        url = self.url.format(user.id)

        self.client.login(
            username=user.email, password=Helpers.USER1["password"])
        response = self.client.delete(url, data=bookmark_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user.bookmarks.all().count(), 1)

    def test_delete_for_multiple_bookmarks_all_existing(self):
        user = Helpers.getUser(Helpers.USER1)
        composition1 = Helpers.createComposition(user)
        composition2 = Helpers.createComposition(user)
        composition3 = Helpers.createComposition(user)
        user.bookmarks.add(composition1, composition2, composition3)
        bookmark_data = {'bookmarks': [composition1.id, composition2.id]}
        url = self.url.format(user.id)

        self.client.login(
            username=user.email, password=Helpers.USER1["password"])
        response = self.client.delete(url, data=bookmark_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user.bookmarks.all().count(), 1)

    def test_delete_for_multiple_bookmarks_all_not_existing(self):
        user = Helpers.getUser(Helpers.USER1)
        composition1 = Helpers.createComposition(user)
        composition2 = Helpers.createComposition(user)
        composition3 = Helpers.createComposition(user)
        composition4 = Helpers.createComposition(user)
        user.bookmarks.add(
            composition1, composition2, composition3, composition4)
        bookmark_data = {
            'bookmarks': [composition2.id, 23, composition1.id, 59, 34]}
        url = self.url.format(user.id)

        self.client.login(
            username=user.email, password=Helpers.USER1["password"])
        response = self.client.delete(url, data=bookmark_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user.bookmarks.all().count(), 2)
