from .client import cloudinary_uploader, cloudinary_utils

def upload_image(image_descriptor, *args, **kwargs):
	# TODO Add eager here for art images
	return cloudinary_uploader.upload(image_descriptor, *args, **kwargs)

def build_url(public_id, *args, **kwargs):
    return cloudinary_utils.cloudinary_url(public_id, *args, **kwargs)
