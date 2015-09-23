from __future__ import division
import os
import util

from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.models import ContentType

from ShowCase.slugger import unique_slugify

from .imageTools import bind_image_resize_handler, WIDTH_READER, WIDTH_STICKY, resized_file_path

from posts.models import Post, bind_post
from feeds.models import Fresh, bind_fresh_feed, Staff, bind_staff_feed

def get_upload_file_name_composition(instance, filename):
    return '%s/%s/%s_%s_thirddime%s' % (instance.uploader.id, slugify(instance.artist.name), slugify(instance.artist.name), slugify(instance.title), '.' + filename.split('.')[-1])

class Composition(models.Model):
    title = models.CharField(max_length=100, blank=False, verbose_name='Title')
    description = models.CharField(
        max_length=1000, blank=True, default='', verbose_name='Description')
    uploader = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='compositions')
    artist = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='arts')
    slug = models.SlugField(max_length=200, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    matter = models.ImageField(upload_to=get_upload_file_name_composition, max_length=500)
    views = models.IntegerField(default=0)
    nsfw = models.BooleanField(default=False)

    class Meta:
        ordering = ('created',)

    def save(self, *args, **kwargs):
        slug_str = "%s %s" % (self.artist.name, self.title)
        unique_slugify(self, slug_str)

        super(Composition, self).save(*args, **kwargs)

        self.make_artist()

    def make_artist(self):
        if not self.artist.is_artist:
            self.artist.is_artist = True
            self.artist.save()

    def add_to_fresh_feed(self):
        Fresh.objects.create(feed_type=Fresh.ART,
            content_object=self)

    def remove_fresh_post(self):
        try:
            Fresh.objects.filter(feed_type=Fresh.ART,
                object_id=self.bucket.id,
                content_type=ContentType.objects.get_for_model(Composition)).delete()
        except:
            pass

    def get_fresh_post(self):
        return Fresh.objects.filter(feed_type=Fresh.ART,
                object_id=self.id,
                content_type=ContentType.objects.get_for_model(Composition))

    def add_to_staff_feed(self):
        Staff.objects.create(feed_type=Staff.ART,
            content_object=self)

    def get_staff_post(self):
        return Staff.objects.filter(feed_type=Staff.ART,
                object_id=self.id,
                content_type=ContentType.objects.get_for_model(Composition))

    def remove_staff_post(self):
        try:
            Staff.objects.filter(feed_type=Staff.ART,
                object_id=self.bucket.id,
                content_type=ContentType.objects.get_for_model(Composition)).delete()
        except:
            pass

    def timesince(self, now=None):
        from django.utils.timesince import timesince as _
        return _(self.created, now)

    def __str__(self):
        if len(self.title) > 10:
            return self.title[:10] + '...'
        else:
            return self.title

    def __unicode__(self):
        if len(self.title) > 10:
            title = self.title[:10] + '...'
        else:
            title = self.title

        return title.encode('utf-8')

    def get_absolute_url(self):
        return "#/compositions/{0}/{1}".format(self.id, self.slug)

    def get_sitemap_url(self):
        return "/arts/{0}".format(self.slug)

    def get_matter_sitemap_url(self):
        return "http://thirddime.com{0}".format(self.matter.url)

    def get_outline_sitemap_url(self):
        url = self.get_outline_url()
        return "http://thirddime.com{0}".format(url)

    def get_grayscale_sitemap_url(self):
        url = self.get_grayscale_url()
        return "http://thirddime.com{0}".format(url)

    def get_outline_url(self):
        return resized_file_path(self.matter.url, 'outline')

    def get_grayscale_url(self):
        return resized_file_path(self.matter.url, 'gray')

    def get_550_url(self):
        return resized_file_path(self.matter.url, WIDTH_READER)

    def get_350_url(self):
        return resized_file_path(self.matter.url, WIDTH_STICKY)

    def get_interpretations_count(self):
        return self.interpretation_set.count()

    def get_matter_aspect(self):
        return self.matter.height/self.matter.width

    def is_nsfw(self, user):
        if user.is_anonymous() or user.nsfw:
            return self.nsfw

        return False

    @property
    def attached_images_path(self):
        return [
            self.matter.path,
            resized_file_path(self.matter.path, WIDTH_STICKY),
            resized_file_path(self.matter.path, WIDTH_READER),
            resized_file_path(self.matter.path, 'outline'),
            resized_file_path(self.matter.path, 'gray'),
        ]

    @property
    def image_path(self):
        return self.matter.path

    def is_bookmarked(self, user_id):
        return self.bookers.filter(id=user_id).exists()

    def has_ownership(self, user_id):
        return self.uploader.id == user_id

    @property
    def bookmarks_count(self):
        return self.bookers.all().count()

    @property
    def buckets_count(self):
        return self.holders.all().count()

    def create_post(self):
        Post.objects.create(
            composition=self,
            creator=self.artist,
            post_type = Post.CREATE,
            content_object=self)

        return Post(
            composition=self,
            creator=self.uploader,
            post_type = Post.ADD,
            content_object=self)

    def get_post(self):
        return Post.objects.filter(composition=self,
            creator=self.artist,
            post_type__in=[POST.ADD, POST.CREATE],
            object_id=self.id,
            content_type=ContentType.objects.get_for_model(self))

#Bind Signals
bind_image_resize_handler(Composition)
bind_post(Composition)
bind_fresh_feed(Composition)
bind_staff_feed(Composition)


# Intrepretation Image

def get_upload_file_name_interpretation_image(instance, filename):
    return '%s/Interprets/%s/%s_meta%s' % (instance.uploader.id, slugify(instance.composition.title),slugify(instance.composition.title), '.' + filename.split('.')[-1])

class InterpretationImage(models.Model):
    UPLOAD = 'UPL'
    CROP = 'CRP'

    SOURCE_TYPE_CHOICES = (
        (UPLOAD, 'upload'),
        (CROP, 'crop'),
    )

    composition = models.ForeignKey(Composition)
    image = models.ImageField(upload_to=get_upload_file_name_interpretation_image)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL)
    source_type = models.CharField(default=UPLOAD, max_length=3, choices=SOURCE_TYPE_CHOICES)

    def get_550_url(self):
        return self.resized_file_path(self.image.url, WIDTH_READER)

    def get_550_path(self):
        return self.resized_file_path(self.image.path, WIDTH_READER)

    def get_350_url(self):
        return self.resized_file_path(self.image.url, WIDTH_STICKY)

    @property
    def attached_images_path(self):
        return [
            self.image.path,
            resized_file_path(self.image.path, WIDTH_STICKY),
            resized_file_path(self.image.path, WIDTH_READER),
        ]

    @property
    def image_path(self):
        return self.image.path


# Bind Signals
bind_image_resize_handler(InterpretationImage)