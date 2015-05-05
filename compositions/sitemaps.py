from django.contrib.sitemaps import Sitemap
from .models import Composition


class CompositionSitemap(Sitemap):
    changefreq = "daily"
    priority = 1

    def items(self):
        return Composition.objects.all()

    def lastmod(self, obj):
        return obj.created

    def location(self, obj):
        return obj.get_sitemap_url()