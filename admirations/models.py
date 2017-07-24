from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from posts.models import Post, bind_post

class AdmirationOption(models.Model):
    word = models.CharField(max_length=50)

class Admiration(models.Model):
    BUCKET = 'BK'
    ART = 'AR'
    INTERPRET = 'IN'

    TYPE_CHOICES = (
        (BUCKET, 'bucket'),
        (ART, 'art'),
        (INTERPRET, 'interpret'),
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='admirations')
    created = models.DateTimeField(auto_now_add=True)
    admire_type = models.CharField(max_length=2, choices=TYPE_CHOICES)
    admire_as = models.ForeignKey(AdmirationOption)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def create_post(self, created, raw):
        if created and not raw:
            if self.admire_type == self.BUCKET:
                post_type = Post.ADMIRE_BUCKET
            elif self.admire_type == self.ART:
                post_type = Post.ADMIRE_ART
            elif self.admire_type == self.INTERPRET:
                post_type = Post.ADMIRE_INTERPRET
            else:
                raise("Invalid admire type found")

            post = Post(
                creator=self.owner,
                post_type = post_type,
                content_object=self.content_object)
            post.save()

    def get_post(self):
        if self.admire_type == self.BUCKET:
            post_type = Post.ADMIRE_BUCKET
        elif self.admire_type == self.ART:
            post_type = Post.ADMIRE_ART
        elif self.admire_type == self.INTERPRET:
            post_type = Post.ADMIRE_INTERPRET
        else:
            raise("Invalid admire type found")

        return Post.objects.filter(
            creator=self.owner,
            post_type=post_type,
            object_id=self.object_id,
            content_type=self.content_type)

bind_post(Admiration)

