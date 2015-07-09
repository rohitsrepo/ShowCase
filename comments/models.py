from django.db import models
from django.conf import settings
from django.utils.timesince import timesince
from interpretations.models import Interpretation


class Comment(models.Model):
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL)
    interpretation = models.ForeignKey(Interpretation, related_name="comments")
    edited = models.BooleanField(default=False)

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
        Returns url of the interpretation it is realted to.
        """

        return self.interpretation.get_absolute_url()
