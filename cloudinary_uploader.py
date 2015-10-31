import os, django, shutil
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ShowCase.settings")
django.setup()

from random import randint

from django.template.defaultfilters import slugify

from compositions.models import Composition
from mediastore.manager import upload_image

def get_public_id(uploader, artist, composition_name):
        return '%s/%s/%s_%s_thirddime_%s' % (slugify(uploader.name),
            slugify(artist.name),
            slugify(artist.name),
            slugify(composition_name),
            randint(1000, 10000))

def upload_and_update(composition):
    matter_public_id = get_public_id(composition.uploader, composition.artist, composition.title)
    matter_meta = upload_image(composition.matter, public_id=matter_public_id, phash = True)

    composition.matter_identifier = matter_meta['public_id']
    composition.matter_height = matter_meta['height']
    composition.matter_width = matter_meta['width']
    composition.matter_format = matter_meta['format']
    composition.matter_phash = matter_meta['phash']

    composition.save()
