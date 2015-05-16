from django.contrib.sitemaps import Sitemap
from .models import User


class ArtistSitemap(Sitemap):
    changefreq = "daily"
    priority = 1

    def items(self):
        return User.objects.filter(is_artist=True)

    def lastmod(self, obj):
        return obj.date_joined

    def location(self, obj):
        return obj.get_sitemap_url()