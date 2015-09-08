from bs4 import BeautifulSoup

from django.db import models
from django.conf import settings
from django.utils.timesince import timesince
from django.contrib.contenttypes.models import ContentType

from compositions.models import Composition
from posts.models import Post, bind_post


class Interpretation(models.Model):
    composition = models.ForeignKey(Composition)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    interpretation = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    public = models.BooleanField(default=False)

    def __str__(self):
        if len(self.interpretation) > 12:
            interpretation = self.interpretation[:12] + '...'
        else:
            interpretation = self.interpretation

        return interpretation

    def __unicode__(self):
        if len(self.interpretation) > 12:
            interpretation = self.interpretation[:12] + '...'
        else:
            interpretation = self.interpretation

        return u'%s' % (interpretation, )

    def timesince(self, now=None):
        return timesince(self.created, now)

    def get_absolute_url(self):
        """
        Returns url of the composition it is realted to.
        """

        return self.composition.get_absolute_url()

    def to_text(self):
        soup = BeautifulSoup(self.interpretation)
        return soup.get_text()

    def create_post(self):
        return Post(
            composition=self.composition,
            creator=self.user,
            post_type = Post.INTERPRET,
            content_object=self)

    def get_post(self):
        return Post.objects.filter(composition=self.composition,
            creator=self.user,
            post_type=POST.INTERPRET,
            object_id=self.id,
            content_type=ContentType.objects.get_for_model(Interpretation))

#Bind Signals
bind_post(Interpretation)