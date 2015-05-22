import os
import util
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from votes.models import Vote
from .utils import GrayScaleAndSketch
from .imageTools import generate_size_versions, WIDTH_READER, WIDTH_STICKY, compress

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
    matter = models.FileField(upload_to=get_upload_file_name_composition)

    class Meta:
        ordering = ('created',)

    def save(self, *args, **kwargs):
        new_instance = False
        if self.pk is None:
            new_instance = True

        slug_str = "%s %s" % (self.artist.name, self.title) 
        util.unique_slugify(self, slug_str)

        super(Composition, self).save(*args, **kwargs)

        self.make_artist()
        if new_instance:
            generate_size_versions(self.matter.path)

    def make_artist(self):
        if not self.artist.is_artist:
            self.artist.is_artist = True
            self.artist.save()

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

    def _format_url(self, suffix):
        file_path, file_name = os.path.split(self.matter.url)
        name, extension = os.path.splitext(file_name)
        return os.path.join(file_path, '{0}_{1}{2}'.format(name, suffix, extension))

    def get_outline_url(self):
        return self._format_url("outline")

    def get_grayscale_url(self):
        return self._format_url("gray")

    def get_550_url(self):
        return self._format_url(WIDTH_READER)

    def get_350_url(self):
        return self._format_url(WIDTH_STICKY)

    def get_interpretations_count(self):
        return self.interpretation_set.count()

# To create vote instance when a compostion is created
@receiver(post_save, sender=Composition)
def create_vote(sender, **kwargs):
    created = kwargs.get('created')
    if created:
        instance = kwargs.get('instance')
        vote = Vote(positive=0, negative=0, composition=instance)
        vote.save()

        GrayScaleAndSketch(instance.matter.path)

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

    def save(self, *args, **kwargs):
        new_instance = False
        if self.pk is None:
            new_instance = True

        super(InterpretationImage, self).save(*args, **kwargs)

        if new_instance:
            compress(self.image.path)
            generate_size_versions(self.image.path)

    def _format_url(self, suffix):
        file_path, file_name = os.path.split(self.image.url)
        name, extension = os.path.splitext(file_name)
        return os.path.join(file_path, '{0}_{1}{2}'.format(name, suffix, extension))

    def _format_path(self, suffix):
        file_path, file_name = os.path.split(self.image.path)
        name, extension = os.path.splitext(file_name)
        return os.path.join(file_path, '{0}_{1}{2}'.format(name, suffix, extension))

    def get_550_url(self):
        return self._format_url(WIDTH_READER)

    def get_550_path(self):
        return self._format_path(WIDTH_READER)

    def get_350_url(self):
        return self._format_url(WIDTH_STICKY)

    def get_350_path(self):
        return self._format_path(WIDTH_STICKY)

# post_delete.connect(util.file_cleanup, sender=InterpretationImage, dispatch_uid="interpretationImage.file_cleanup")

# To create vote instance when a compostion is created
@receiver(post_delete, sender=InterpretationImage)
def remove_files(sender, **kwargs):
    instance = kwargs.get('instance')

    os.remove(unicode(instance.image.path))
    os.remove(unicode(instance.get_550_path()))
    os.remove(unicode(instance.get_350_path()))
