import os
from PIL import Image
from django.db.models.signals import post_delete, post_save

WIDTH_PROFILE = 120

def resize_picture_path(filename, width):
    file, ext = os.path.splitext(filename)
    if not ext:
        ext = '.png'
    return file + "_" + str(width) + ext

def _resize(im, width, filename):
    resize_ratio = width/float(im.size[0])
    height = im.size[1]*resize_ratio
    size = (width, height)
    im.thumbnail(size)

    resize_filepath = resize_picture_path(filename, width)
    im.save(resize_filepath)

def resize_profile(filepath):
    im = Image.open(filepath)
    _resize(im.copy(), WIDTH_PROFILE, filepath)

def user_created(sender, instance, created, raw, **kwargs):
    #TODO this should not happen on every save
    #TODO delete old file on picture update
    if not instance.has_default_picture():
        resize_profile(instance.picture.path)

def user_delete(sender, instance, **kwargs):
    if not instance.has_default_picture():
        try:
            os.remove(unicode(instance.picture.path))
            os.remove(unicode(resize_picture_path(instance.picture.path, WIDTH_PROFILE)))
        except:
            pass

def bind_profile_picture_handler(sender, **kwargs):
    post_save.connect(user_created, sender=sender)
    post_delete.connect(user_delete, sender=sender)