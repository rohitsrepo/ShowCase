from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class BookMark(models.Model):
    BUCKET = 'BK'
    ART = 'AR'

    TYPE_CHOICES = (
        (BUCKET, 'bucket'),
        (ART, 'art'),
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='bookmarks')
    created = models.DateTimeField(auto_now_add=True)
    bookmark_type = models.CharField(max_length=2, choices=TYPE_CHOICES)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
