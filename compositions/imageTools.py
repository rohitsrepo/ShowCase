import os
from PIL import Image

WIDTH_STICKY = 350
WIDTH_READER = 550

def _resize(im, width, filename):
	resize_ratio = width/float(im.size[0])
	height = im.size[1]*resize_ratio
	size = (width, height)
	im.thumbnail(size)

	file, ext = os.path.splitext(filename)
	im.save(file + "_" + str(width) + ext)

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