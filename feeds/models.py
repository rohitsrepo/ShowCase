from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, post_delete
from django.contrib.contenttypes.fields import GenericForeignKey

from interpretations.models import Interpretation


class StaffPost(models.Model):
    composition = models.ForeignKey('compositions.Composition')
    interpretation = models.ForeignKey(Interpretation)


    def get_search_parameter(self):
        return 'feed=editors&post={0}'.format(self.id)

class Fresh(models.Model):
    BUCKET = 'BK'
    ART = 'AR'

    TYPE_CHOICES = (
        (ART, 'art'),
        (BUCKET, 'bucket'),
    )

    created = models.DateTimeField(auto_now_add=True)
    public = models.BooleanField(default=True)
    feed_type = models.CharField(max_length=2, choices=TYPE_CHOICES)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


# Define Signals
def model_created(sender, instance, created, raw, **kwargs):
    if created:
        instance.add_to_fresh_feed()

def model_deleted(sender, instance, **kwargs):
    try:
        instance.remove_fresh_post().delete()
    except:
        pass

def bind_fresh_feed(sender, **kwargs):
    post_save.connect(model_created, sender=sender)
    post_delete.connect(model_deleted, sender=sender)

class Staff(models.Model):
    BUCKET = 'BK'
    ART = 'AR'

    TYPE_CHOICES = (
        (ART, 'art'),
        (BUCKET, 'bucket'),
    )

    created = models.DateTimeField(auto_now_add=True)
    public = models.BooleanField(default=True)
    feed_type = models.CharField(max_length=2, choices=TYPE_CHOICES)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


# Define Signals
def model_deleted_staff(sender, instance, **kwargs):
    try:
        instance.remove_staff_post().delete()
    except:
        pass

def bind_staff_feed(sender, **kwargs):
    post_delete.connect(model_deleted_staff, sender=sender)