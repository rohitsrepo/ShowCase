import os
from PIL import Image
from .utils import GrayScaleAndSketch
from django.db.models.signals import post_delete, post_save
from colorTools import colorz

WIDTH_STICKY = 350
WIDTH_READER = 550

def resized_file_path(filename, width):
    file, ext = os.path.splitext(filename)
    return file + "_" + str(width) + ext

def _resize(im, width, filename):
    resize_ratio = width/float(im.size[0])
    height = im.size[1]*resize_ratio
    size = (width, height)
    im.thumbnail(size)

    resized_filepath = resized_file_path(filename, width)
    if im.mode != "RGB":
        im = im.convert("RGB")
    im.save(resized_filepath)

def generate_size_versions(filepath):
    im = Image.open(filepath)
    _resize(im.copy(), WIDTH_READER, filepath)
    _resize(im.copy(), WIDTH_STICKY, filepath)

def compress(filepath, quality=80):
    im = Image.open(filepath)
    im.save(filepath, quality=quality, optimize=True, progressive=True)

def crop(filepath, box):
    im = Image.open(filepath)
    im_crop = im.crop(box);

    file, ext = os.path.splitext(filepath)
    cropped_file = file + "_" + "crop" + ext
    im_crop.save(cropped_file)
    return cropped_file

def image_model_created(sender, instance, created, raw, **kwargs):
    if created and not raw:
        generate_size_versions(instance.image_path)
        major = colorz(instance.matter.path)
        instance.major = major[0]
        instance.save()
        GrayScaleAndSketch(instance.image_path)

def image_model_delete(sender, instance, **kwargs):
    for image_path in instance.attached_images_path:
        try:
            os.remove(unicode(image_path))
        except:
            pass

def bind_image_resize_handler(sender, **kwargs):
    post_save.connect(image_model_created, sender=sender)
    post_delete.connect(image_model_delete, sender=sender)
