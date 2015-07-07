from django.db import models
from django.conf import settings
from django.utils.timesince import timesince
from posts.models import Post


class PostComment(models.Model):
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL)
    post = models.ForeignKey(Post)
    edited = models.BooleanField(default=False)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        if len(self.comment) > 12:
            comment = self.comment[:12] + '...'
        else:
            comment = self.comment

        return comment

    def timesince(self, now=None):
        return timesince(self.created, now)

    def get_absolute_url(self):
        """
        Returns url of the post it is realted to.
        """

        return self.Post.get_absolute_url()