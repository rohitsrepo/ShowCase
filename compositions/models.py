from django.db import models
from django.conf import settings


def get_upload_file_name_composition(instance, filename):
    	return 'Users/%s/Compositions/%s/%s' % (instance.artist.id, instance.id, filename)


def get_upload_file_name_matter(instance, filename):
    	return 'Users/%s/Compositions/%s/%s' % (instance.artist.id, instance.id, filename)


class Composition(models.Model):

    AUDIO = 'AU'
    VIDEO = 'VI'
    IMAGE = 'IM'
    TYPE_CHOICES = (
	    (AUDIO, 'Audio'),
	    (VIDEO, 'Video'),
	    (IMAGE, 'Image')
	    )

    title = models.CharField(max_length=100, blank=False, verbose_name='Title')
    description = models.CharField(max_length=1000, blank=True, default='', verbose_name='Description')
    artist = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='compositions')
    created = models.DateTimeField(auto_now_add=True)
    content_type = models.CharField(max_length=6, choices=TYPE_CHOICES, default=IMAGE, verbose_name='Type')
    display_image = models.ImageField(upload_to=get_upload_file_name_composition, default=settings.DEFAULT_COMPOSITION_IMAGE_PICTURE, blank=True)
    matter = models.FileField(upload_to=get_upload_file_name_matter)

    class Meta:
        ordering = ('created',)

    def timesince(self, now=None):
        from django.utils.timesince import timesince as _
	return _(self.created, now)
