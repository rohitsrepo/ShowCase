"""
Django settings for ShowCase project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'y2dx1lvq(_n19_dap%l0fw#ouyiu8g0dq!h)=t4=-7d#dqqum6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'ShowCase/templates'),
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "ShowCase/static"),
)

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'accounts',
    'compositions',
    'votes',
    'interpretationVotes',
    'comments',
    'notifications',
    'messaging',
    'search',
    'interpretations',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'ShowCase.urls'

WSGI_APPLICATION = 'ShowCase.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../database/showCase_db.sqlite3'),
    }
}

SOUTH_MIGRATION_MODULES = {
    'taggit': 'taggit.south_migrations',
}


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(BASE_DIR, '../static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

AUTH_USER_MODEL = 'accounts.User'
LOGIN_REDIRECT_URL = '/'

DEFAULT_USER_PICTURE = MEDIA_URL + 'root/user_default.jpg'
DEFAULT_COMPOSITION_IMAGE_PICTURE = MEDIA_URL + \
    'root/composition_image_default.jpg'
DEFAULT_COMPOSITION_AUDIO_PICTURE = MEDIA_URL + \
    'root/composition_audio_default.jpg'
DEFAULT_COMPOSITION_VIDEO_PICTURE = MEDIA_URL + \
    'root/composition_video_default.jpg'

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',)
}

APPEND_SLASH = False

SHOWCASE_ACCOUNT = 'art.showcase.v1.0@gmail.com'
SHOWCASE_PASSWORD = 'showcaseiitkgp'
MAIL_SENDER = 'ShowCase'
