from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify


def get_upload_file_name_composition(instance, filename):
    	return 'Users/%s/Compositions/%s/%s' % (instance.artist.id, instance.created, filename)


class Composition(models.Model):
    title = models.CharField(max_length=100, blank=False, verbose_name='Title')
    description = models.CharField(max_length=1000, blank=True, default='', verbose_name='Description')
    artist = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='compositions')
    slug = models.SlugField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    matter = models.FileField(upload_to=get_upload_file_name_composition)

    class Meta:
        ordering = ('created',)

    def save(self, *args, **kwargs):
	if not self.pk:
	    self.slug = slugify(self.title)
	super(Composition, self).save(*args, **kwargs)

    def timesince(self, now=None):
        from django.utils.timesince import timesince as _
	return _(self.created, now)
