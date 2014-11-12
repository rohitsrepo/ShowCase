from django.db import models
from django.conf import settings


class InterpretationVote(models.Model):
    positive = models.PositiveIntegerField(default=0)
    negative = models.PositiveIntegerField(default=0)
    interpretation = models.OneToOneField(
        'interpretations.Interpretation', related_name='vote')
    voters = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='interpretationVotes')

    def __str__(self):
        return 'Vote: + %i - %i : Interpretation: %s' % (self.positive, self.negative, self.interpretation)

    def has_voted(self, user):
        if self.voters.filter(id=user.id).exists():
            return True
        return False

    def add_voter(self, user):
        if self.has_voted(user):
            raise Exception(
                'User has already voted. Please handle this exception while defining voting endpoint and return proper message to the request.')

        self.voters.add(user)

    def vote_positive(self, user):
        self.add_voter(user)
        self.positive += 1
        self.save()

    def vote_negative(self, user):
        self.add_voter(user)
        self.negative += 1
        self.save()

    def get_absolute_url(self):
        """
        Return url for the interpretation it is related to.
        """

        return self.interpretation.get_absolute_url()
