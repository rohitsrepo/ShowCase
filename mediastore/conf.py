import django
from django.conf import settings

API_KEY = getattr(settings, 'CLOUDINARY_API_KEY', None)
API_SECRET = getattr(settings, 'CLOUDINARY_API_SECRET', None)
CLOUDNAME = getattr(settings, 'CLOUDINARY_CLOUDNAME', None)