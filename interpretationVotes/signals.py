from django.db.models.signals import post_save
from django.dispatch import receiver
from interpretations.models import Interpretation
from interpretationVotes.models import InterpretationVote


# To create vote instance when a compostion is created
@receiver(post_save, sender=Interpretation)
def create_vote(sender, **kwargs):
    created = kwargs.get('created')
    if created:
        instance = kwargs.get('instance')
        vote = InterpretationVote(positive=0, negative=0, interpretation=instance)
        vote.save()
