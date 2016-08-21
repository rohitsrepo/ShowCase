from django.contrib import sitemaps
from django.core.urlresolvers import reverse

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.7
    changefreq = 'monthly'

    def items(self):
        return ['about', 'contact', 'guidelines', 'register', 'login', 'composition-upload']

    def location(self, item):
        return reverse(item)


class ReaderSitemap(sitemaps.Sitemap):
    priority = 1
    changefreq = 'always'

    def items(self):
        return ['reader']

    def location(self, item):
        return reverse(item)