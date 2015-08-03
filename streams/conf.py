import django
from django.conf import settings

API_KEY = getattr(settings, 'STREAM_API_KEY', None)
API_SECRET = getattr(settings, 'STREAM_API_SECRET', None)
LOCATION = getattr(settings, 'STREAM_LOCATION', None)


USER_FEED = getattr(settings, 'STREAM_USER_FEED', 'user')
NEWS_FEEDS = getattr(settings, 'STREAM_NEWS_FEEDS',
    {'flat':'flat', 'aggregated':'aggregated'}
)
NOTIFICATION_FEED = getattr(settings, 'STREAM_PERSONAL_FEED', 'notification')