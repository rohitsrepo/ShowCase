import re, os
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from votes.models import Vote
from .utils import GrayScaleAndSketch
from .imageTools import generate_size_versions, WIDTH_READER, WIDTH_STICKY

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
        slug_str = "%s %s" % (self.artist.name, self.title) 
        unique_slugify(self, slug_str) 
        super(Composition, self).save(*args, **kwargs)
        self.make_artist()
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

def unique_slugify(instance, value, slug_field_name='slug', queryset=None,
                   slug_separator='-'):
    slug_field = instance._meta.get_field(slug_field_name)

    slug = getattr(instance, slug_field.attname)
    slug_len = slug_field.max_length

    # Sort out the initial slug, limiting its length if necessary.
    slug = slugify(value)
    if slug_len:
        slug = slug[:slug_len]
    slug = _slug_strip(slug, slug_separator)
    original_slug = slug

    # Create the queryset if one wasn't explicitly provided and exclude the
    # current instance from the queryset.
    if queryset is None:
        queryset = instance.__class__._default_manager.all()
    if instance.pk:
        queryset = queryset.exclude(pk=instance.pk)

    # Find a unique slug. If one matches, at '-2' to the end and try again
    # (then '-3', etc).
    next = 2
    while not slug or queryset.filter(**{slug_field_name: slug}):
        slug = original_slug
        end = '%s%s' % (slug_separator, next)
        if slug_len and len(slug) + len(end) > slug_len:
            slug = slug[:slug_len-len(end)]
            slug = _slug_strip(slug, slug_separator)
        slug = '%s%s' % (slug, end)
        next += 1

    setattr(instance, slug_field.attname, slug)


def _slug_strip(value, separator='-'):
    separator = separator or ''
    if separator == '-' or not separator:
        re_sep = '-'
    else:
        re_sep = '(?:-|%s)' % re.escape(separator)
    # Remove multiple instances and if an alternate separator is provided,
    # replace the default '-' separator.
    if separator != re_sep:
        value = re.sub('%s+' % re_sep, separator, value)
    # Remove separator from the beginning and end of the slug.
    if separator:
        if separator != '-':
            re_sep = re.escape(separator)
        value = re.sub(r'^%s+|%s+$' % (re_sep, re_sep), '', value)
    return value