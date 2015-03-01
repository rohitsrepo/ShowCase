from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from compositions.models import Composition
from django.conf import settings
from django.utils.timesince import timesince
from interpretationVotes.models import InterpretationVote
from feeds.models import FreshPost


class Interpretation(models.Model):
    composition = models.ForeignKey(Composition)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    interpretation = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if len(self.interpretation) > 12:
            interpretation = self.interpretation[:12] + '...'
        else:
            interpretation = self.interpretation

        return interpretation

    def timesince(self, now=None):
        return timesince(self.created, now)

    def get_absolute_url(self):
        """
        Returns url of the composition it is realted to.
        """

        return self.composition.get_absolute_url()



# To create vote instance when an interpretatoin is created
@receiver(post_save, sender=Interpretation)
def create_vote(sender, **kwargs):
    created = kwargs.get('created')
    if created:
        instance = kwargs.get('instance')
        vote = InterpretationVote(positive=0, negative=0, interpretation=instance)
        vote.save()
        
#To create FreshPost instance whenever a new interpretation is created
@receiver(post_save, sender=Interpretation)
def create_freshpost_from_Interpretation(sender, **kwargs):
    created = kwargs.get('created', False)
    if created:
        interpretation_instance = kwargs.get('instance')
        composition_instance = interpretation_instance.composition
        fresh_post = FreshPost(composition=composition_instance, interpretation= interpretation_instance)
        fresh_post.save()
