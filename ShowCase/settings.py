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

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
    },
]

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'ShowCase/templates'),
)

## settings.py
TEMPLATE_CONTEXT_PROCESSORS = (
    #default
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    # Added later
    'django.core.context_processors.request',
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "ShowCase/static"),
)

ALLOWED_HOSTS = []

# Application definition
SITE_ID = 1

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'rest_framework',
    'accounts',
    'compositions',
    'votes',
    'interpretationVotes',
    'comments',
    'interpretations',
    'feeds',
    'contentManager',
    'posts',
    'postVotes',
    'postComments',
    'allaccess',
    'streams',
    'buckets',
    'bookmarks',
    'admirations',
    'follow',
    'djcelery',
    'mediastore',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allaccess.backends.AuthorizedServiceBackend',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',
)

ROOT_URLCONF = 'ShowCase.urls'

WSGI_APPLICATION = 'ShowCase.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'thirddime',
        'USER': 'thirduser',
        'PASSWORD': 'sir_newton_third',
        'HOST': 'localhost',
        'PORT': '3306',
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
MEDIA_ROOT = os.path.join(BASE_DIR, '../media')

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
LOGIN_URL = '/login/'

DEFAULT_USER_PICTURE = STATIC_URL + 'images/user_default.jpg'

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',)
}

APPEND_SLASH = False

POSTS_PER_PAGE = 10

STREAM_API_KEY = 'x399sdbsgtmx'
STREAM_API_SECRET = 'njhq6uzms7bezq6hxwsz434b6xpp37r97nwc3bg99ps8cmgrf6qvqhyjmgdbuhe9'

CLOUDINARY_API_KEY = '999275522129416'
CLOUDINARY_API_SECRET = 'Q-w9Rg23en1wmvK-3cNywKnqpcw'
CLOUDINARY_CLOUDNAME = 'danufntls'

EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
DEFAULT_FROM_EMAIL = 'ThirdDime Team <info@thirddime.com>'

SERVER_EMAIL = 'Server Logs <server@thirddime.com>'
ADMINS = (('Rohit', 'rgarg1992@gmail.com'),)
MANAGERS = (('Rohit', 'rgarg1992@gmail.com'),)

CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'
CELERY_TASK_RESULT_EXPIRES=3600