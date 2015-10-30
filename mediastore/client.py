import os
import cloudinary
import cloudinary.uploader
import cloudinary.api

from django.core.exceptions import ImproperlyConfigured

from . import conf

if conf.API_KEY and conf.API_SECRET and conf.CLOUDNAME:
    cloudinary.config( 
						  cloud_name = conf.CLOUDNAME, 
						  api_key = conf.API_KEY, 
						  api_secret = conf.API_SECRET
						)

    cloudinary_uploader = cloudinary.uploader

else:
    raise ImproperlyConfigured('Cloudinary credentials are not set in your settings')