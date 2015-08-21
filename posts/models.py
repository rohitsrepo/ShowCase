from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from streams.manager import bind_stream
from postVotes.models import PostVote, bind_post_vote

class Post(models.Model):
    INTERPRET = 'IN'
    ADD = 'AD'
    CREATE = 'CR'
    BUCKET = 'BK'

    TYPE_CHOICES = (
        (INTERPRET, 'interpret'),
        (ADD, 'add'),
        (CREATE, 'create'),
        (BUCKET, 'bucket'),
    )

    composition = models.ForeignKey('compositions.Composition', related_name='posts')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_posts')
    created = models.DateTimeField(auto_now_add=True)
    public = models.BooleanField(default=True)
    post_type = models.CharField(max_length=2, choices=TYPE_CHOICES)
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

    @property
    def activity_actor_id(self):
        return self.creator.id

    @property
    def activity_foreign_id(self):
        return self.id

    def create_activity(self):
        activity = dict(
            actor=self.creator.id,
            verb=self.post_type,
            object=self.object_id,
            target=self.composition.id,
            foreign_id=self.id,
            time=self.created,
        )
        return activity

    def create_post_vote(self):
        return PostVote(positive=0, negative=0, post=self)

# Define Signals
def model_created(sender, instance, created, raw, **kwargs):
    if created:
        post = instance.create_post()
        post.save()

def model_deleted(sender, instance, **kwargs):
    try:
        ctype = ContentType.objects.get_for_model(instance)
        post = Post.objects.get(content_type = ctype, object_id = instance.id)
    except:
        pass

def bind_post(sender, **kwargs):
    post_save.connect(model_created, sender=sender)
    post_delete.connect(model_deleted, sender=sender)

# Bind Signals
bind_stream(Post)
bind_post_vote(Post)

# Remove underlying object when deleted
@receiver(post_delete, sender=Post)
def remove_post_target(sender, **kwargs):
    try:
        instance = kwargs.get('instance')
        instance.content_object.delete()
    except:
        pass
