from .client import cloudinary_uploader

def upload_image(image_descriptor, *args, **kwargs):
	# TODO Add eager here for art images
	return cloudinary_uploader.upload(image_descriptor, *args, **kwargs)

