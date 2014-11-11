from django.db import models
from compositions.models import Composition
from django.conf import settings
from django.utils.timesince import timesince


class Interpretation(models.Model):
    composition = models.ForeignKey(Composition)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    interpretation = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if len(self.interpretation) > 12:
            interpretation = self.interpretation[:12] + '...'
        else:
            interpretation = self.interpretation

        return interpretation

    def timesince(self, now=None):
        return timesince(self.created, now)

    def get_absolute_url(self):
        """
        Returns url of the composition it is realted to.
        """

        return self.composition.get_absolute_url()
