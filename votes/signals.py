from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from compositions.models import Composition
from votes.models import Vote

#To ensure Vote entry gets deleted when a Composition is deleted.
@receiver(pre_delete, sender=Composition)
def delete_vote(sender, **kwargs):
    instance = kwargs.get('instance')
    instance.vote.delete()
