from rest_framework.test import APITestCase
from rest_framework import status
from api_test import Helpers
from interpretationVotes.models import InterpretationVote
from interpretationVotes import signals


class TestVotes(APITestCase):

    """ Tests for composition votes."""
    url = "/compositions/{0}/interpretations/{1}/votes"

    def createVote(self):
        interpretation = Helpers.createInterpretation()
        return InterpretationVote.objects.get(interpretation=interpretation)

    def castVote(self, vote, favor=True, user=None):
        if user:
            try:
                vote.vote_positive(user) if favor else vote.vote_negative(user)
                return
            except:
                raise Exception(
                    "Error voting: user {} have already voted".format(user.id))

        available_users = (Helpers.USER1, Helpers.USER2, Helpers.USER3)
        for user in available_users:
            registered_user = Helpers.getUser(user)
            try:
                vote.vote_positive(registered_user) if favor else vote.vote_negative(
                    registered_user)
                return
            except:
                pass

        raise Exception(
            "Error voting: all the registered users have already voted.")

    def createResponse(self, interpretation_id, positive, negative):
        return {'positive': positive, 'negative': negative, 'interpretation': interpretation_id}

    def refreshFromDB(self, vote):
        return InterpretationVote.objects.get(id=vote.id)

    def test_get_returns_votes_for_non_autheticated_user(self):
        vote = self.createVote()
        self.castVote(vote, True)
        self.castVote(vote, False)
        url = self.url.format(vote.interpretation.composition.id, vote.interpretation.id)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, self.createResponse(vote.interpretation.id, 1, 1))
        vote = self.refreshFromDB(vote)
        self.assertEqual(vote.positive, 1)
        self.assertEqual(vote.negative, 1)

    def test_get_returns_votes_for_autheticated_user(self):
        user = Helpers.getUser(Helpers.USER1)
        vote = self.createVote()
        self.castVote(vote, True)
        self.castVote(vote, True)
        url = self.url.format(vote.interpretation.composition.id, vote.interpretation.id)

        self.client.login(
            username=user.email, password=Helpers.USER2["password"])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, self.createResponse(vote.interpretation.id, 2, 0))
        vote = self.refreshFromDB(vote)
        self.assertEqual(vote.positive, 2)
        self.assertEqual(vote.negative, 0)

    def test_get_is_idempotent(self):
        user = Helpers.getUser(Helpers.USER1)
        vote = self.createVote()
        self.castVote(vote, True)
        self.castVote(vote, True)
        url = self.url.format(vote.interpretation.composition.id, vote.interpretation.id)

        self.client.login(
            username=user.email, password=Helpers.USER1["password"])
        self.client.get(url)
        self.client.get(url)
        self.client.get(url)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, self.createResponse(vote.interpretation.id, 2, 0))
        vote = self.refreshFromDB(vote)
        self.assertEqual(vote.positive, 2)
        self.assertEqual(vote.negative, 0)

    def test_post_throws_forbidden_for_non_authenticated_user(self):
        Helpers.getUser(Helpers.USER1)
        vote = self.createVote()
        vote_data = {"id": vote.id, "vote": True}
        url = self.url.format(vote.interpretation.composition.id, vote.interpretation.id)

        response = self.client.post(url, vote_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        vote = self.refreshFromDB(vote)
        self.assertEqual(vote.positive, 0)
        self.assertEqual(vote.negative, 0)
        self.assertEqual(vote.voters.all().count(), 0)

    def test_post_throws_unauthrized_for_authenticated_user_who_has_already_voted(self):
        user = Helpers.getUser(Helpers.USER1)
        vote = self.createVote()
        self.castVote(vote, False, user)
        vote_data = {"id": vote.id, "vote": True}
        url = self.url.format(vote.interpretation.composition.id, vote.interpretation.id)

        self.client.login(
            username=user.email, password=Helpers.USER1["password"])
        response = self.client.post(url, vote_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        vote = self.refreshFromDB(vote)
        self.assertEqual(vote.positive, 0)
        self.assertEqual(vote.negative, 1)

    def test_post_works_for_authenticated_user_that_has_not_already_voted(self):
        user = Helpers.getUser(Helpers.USER1)
        vote = self.createVote()
        vote_data = {"id": vote.id, "vote": True}
        url = self.url.format(vote.interpretation.composition.id, vote.interpretation.id)

        self.client.login(
            username=user.email, password=Helpers.USER1["password"])
        response = self.client.post(url, vote_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, self.createResponse(vote.interpretation.id, 1, 0))
        vote = self.refreshFromDB(vote)
        self.assertEqual(vote.positive, 1)
        self.assertEqual(vote.negative, 0)
        self.assertEqual(vote.voters.filter(id=user.id).exists(), True)

    def test_post_works_for_multiple_authenticated_user_that_has_not_already_voted(self):
        user1 = Helpers.getUser(Helpers.USER1)
        user2 = Helpers.getUser(Helpers.USER2)
        user3 = Helpers.getUser(Helpers.USER3)
        vote = self.createVote()
        vote_data1 = {"id": vote.id, "vote": True}
        vote_data2 = {"id": vote.id, "vote": False}
        vote_data3 = {"id": vote.id, "vote": True}
        url = self.url.format(vote.interpretation.composition.id, vote.interpretation.id)

        self.client.login(
            username=user1.email, password=Helpers.USER1["password"])
        response = self.client.post(url, vote_data1)
        self.client.logout()

        self.client.login(
            username=user2.email, password=Helpers.USER2["password"])
        response = self.client.post(url, vote_data2)
        self.client.logout()

        self.client.login(
            username=user3.email, password=Helpers.USER3["password"])
        response = self.client.post(url, vote_data3)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, self.createResponse(vote.interpretation.id, 2, 1))
        vote = self.refreshFromDB(vote)
        self.assertEqual(vote.positive, 2)
        self.assertEqual(vote.negative, 1)
        self.assertEqual(vote.voters.all().count(), 3)
