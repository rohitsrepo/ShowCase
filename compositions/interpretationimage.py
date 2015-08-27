import util
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import models
from django.conf import settings
from .imageTools import bind_image_resize_handler, WIDTH_READER, WIDTH_STICKY, resized_file_path
from .models import Composition
from django.template.defaultfilters import slugify


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
