from django.db.models.signals import post_save
from django.dispatch import receiver
from compositions.models import Composition
from votes.models import Vote


# To create vote instance when a compostion is created
@receiver(post_save, sender=Composition)
def create_vote(sender, **kwargs):
    created = kwargs.get('created')
    if created:
        instance = kwargs.get('instance')
        vote = Vote(positive=0, negative=0, composition=instance)
        vote.save()
