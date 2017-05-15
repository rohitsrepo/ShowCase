from bs4 import BeautifulSoup

from django.db import models
from django.conf import settings
from django.utils.timesince import timesince
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

from ShowCase.slugger import unique_slugify

from posts.models import Post, bind_post

from bookmarks.models import BookMark
from admirations.models import Admiration


class Interpretation(models.Model):
    composition = models.ForeignKey('compositions.Composition', related_name="interprets")
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    interpretation = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    public = models.BooleanField(default=False)
    is_draft = models.BooleanField(default=True)
    slug = models.SlugField(max_length=200, default="")
    bookers = GenericRelation(BookMark, related_query_name='booked_interprets')
    admirers = GenericRelation(Admiration, related_query_name='admired_interprets')

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

    def save(self, *args, **kwargs):
        slug_str = self.get_text(40)
        unique_slugify(self, slug_str)
        super(Interpretation, self).save(*args, **kwargs)

    def timesince(self, now=None):
        return timesince(self.created, now)

    def get_absolute_url(self):
        return '/@' + self.user.slug + '/tales/' + self.slug

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

    def getNotificationTarget(self, post):
        if post.post_type == Post.INTERPRET:
            targets = [self.composition.artist]
            if not (self.composition.artist.id == self.composition.uploader.id):
                targets.append(self.composition.uploader)
        elif post.post_type == Post.ADMIRE_INTERPRET:
            targets = [self.user]

        return targets

    def short_text(self):
        return self.get_text(150)

    def get_text(self, length):
        text = self.to_text()
        if len(text) > length:
            space = text[:length].rfind(" ")
            text = text[:space] + "..."

        return text


    def is_bookmarked(self, user_id):
        return self.bookers.filter(owner=user_id).exists()

    @property
    def bookmarks_count(self):
        return self.bookers.count()

    def is_admired(self, user_id):
        return self.admirers.filter(owner=user_id).exists()

    @property
    def admirers_count(self):
        return self.admirers.count()

#Bind Signals
bind_post(Interpretation)