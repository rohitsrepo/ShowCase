from django.db import models
from django.conf import settings
from django.db.models.signals import post_save

class PostVote(models.Model):
    positive = models.PositiveIntegerField(default=0)
    negative = models.PositiveIntegerField(default=0)
    post = models.OneToOneField('posts.Post', related_name='vote')
    voters = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through='PostVoteMembership')

    def __str__(self):
        return 'Vote: + %i - %i : Post: %s' % (self.positive, self.negative, self.post)

    def has_voted(self, user):
        if self.voters.filter(id=user.id).exists():
            return True
        return False

    def add_voter(self, user, voteType):
        if self.has_voted(user):
            raise Exception(
                'User has already voted. Please handle this exception while defining voting endpoint and return proper message to the request.')

        PostVoteMembership.objects.create(user=user, vote=self, voteType=voteType)

    def vote_positive(self, user):
        self.add_voter(user, True)
        self.positive += 1
        self.save()

    def vote_negative(self, user):
        self.add_voter(user, False)
        self.negative += 1
        self.save()

    def get_voting_status(self, user):
        try:
            voteType = PostVoteMembership.objects.get(vote=self, user=user).voteType
            if(voteType):
                return "Positive"
            return "Negative"
        except:
            return "NotVoted"

    def get_total(self):
        return self.positive - self.negative

    def get_absolute_url(self):
        """
        Return url for the post it is related to.
        """

        return self.post.get_absolute_url()

#Define Signals
def model_created(sender, instance, created, raw, **kwargs):
    if created:
        vote = instance.create_post_vote()
        vote.save()

def bind_post_vote(sender, **kwargs):
    post_save.connect(model_created, sender=sender)

class PostVoteMembership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='vote_membership')
    vote = models.ForeignKey(PostVote)
    voteType = models.BooleanField(default=True)