from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from compositions.models import Composition

class Post(models.Model):
    composition = models.ForeignKey(Composition, related_name='posts')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_posts')
    created = models.DateTimeField(auto_now_add=True)
    public = models.BooleanField(default=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def timesince(self, now=None):
        from django.utils.timesince import timesince as _
        return _(self.created, now)

    def get_comments_count(self):
        return self.comments.all().count()

    def get_voting_status(self, user):
        return self.vote.get_voting_status(user)


# To create vote instance when an post is created
@receiver(post_save, sender=Post)
def create_post_vote(sender, **kwargs):
    created = kwargs.get('created')
    if created:
        instance = kwargs.get('instance')
        vote = PostVote(positive=0, negative=0, post=instance)
        vote.save()