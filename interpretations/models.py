from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from compositions.models import Composition
from django.conf import settings
from django.utils.timesince import timesince
from interpretationVotes.models import InterpretationVote
from posts.models import Post
from bs4 import BeautifulSoup


class Interpretation(models.Model):
    composition = models.ForeignKey(Composition)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    interpretation = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    public = models.BooleanField(default=False)

    def __str__(self):
        if len(self.interpretation) > 12:
            interpretation = self.interpretation[:12] + '...'
        else:
            interpretation = self.interpretation

        return interpretation

    def __unicode__(self):
        if len(self.interpretation) > 12:
            interpretation = self.interpretation[:12] + '...'
        else:
            interpretation = self.interpretation

        return u'%s' % (interpretation, )

    def timesince(self, now=None):
        return timesince(self.created, now)

    def get_absolute_url(self):
        """
        Returns url of the composition it is realted to.
        """

        return self.composition.get_absolute_url()

    def to_text(self):
        soup = BeautifulSoup(self.interpretation)
        return soup.get_text()



# To create vote instance when an interpretatoin is created
@receiver(post_save, sender=Interpretation)
def create_post(sender, **kwargs):
    created = kwargs.get('created')
    if created:
        instance = kwargs.get('instance')
        vote = Post(
            composition=instance.composition,
            creator=instance.user,
            content_object=instance)
        vote.save()