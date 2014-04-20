from django.db.models.signals import post_save
from django.dispatch import receiver
from compositions.models import Composition
from votes.models import Vote


# To create vote instance when a compostion is created
@receiver(post_save, sender=Composition)
def create_vote(sender, **kwargs):
    print "Post Save triggered"
    created = kwargs.get('created')
    if created:
	print "Instance Created"
        instance = kwargs.get('instance')
        vote = Vote(positive=0, negative=0, composition=instance)
        vote.save()
