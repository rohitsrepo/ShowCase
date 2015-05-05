from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from compositions import clientViews


from django.contrib import admin
admin.autodiscover()

# WebClient urls
urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', TemplateView.as_view(template_name='reader.html'), name='reader'),
                       url(r'^about-us$', TemplateView.as_view(template_name='aboutus.html'), name="about"),
                       url(r'^guidelines$', TemplateView.as_view(template_name='guidelines.html'), name='guidelines'),
                       url(r'^contact-us$', TemplateView.as_view(template_name='contactus.html'), name="contact"),
                       url(r'^register$', TemplateView.as_view(template_name='register.html'), name="register"),
                       url(r'^login$', TemplateView.as_view(template_name='login.html'), name="login"),
                       url(r'^upload-art$', TemplateView.as_view(template_name='upload.html'), name="upload"),
                       url(r'^arts/(?P<slug>[\w-]+)$', 'compositions.clientViews.composition_main', name="composition-page"),
		       )

# API urls
urlpatterns += patterns('',
                       url(r'^users', include('accounts.urls')),
                       url(r'^compositions', include('compositions.urls')),
                       url(r'^feeds', include('feeds.urls')),
                       url(r'^content', include('contentManager.urls')),
		       )

# Robots.txt
urlpatterns += patterns('',
                       url(r'^robots.txt$', TemplateView.as_view(template_name='robots.txt'), name='robots'),
    )

# SitesMap
from compositions.sitemaps import CompositionSitemap
from ShowCase.sitemaps import ReaderSitemap, StaticViewSitemap
from django.contrib.sitemaps import views

sitemaps = {
    'reader': ReaderSitemap,
    'compositions': CompositionSitemap,
    'static': StaticViewSitemap
}

urlpatterns += patterns('',
        url(r'^sitemap\.xml$', views.index, {'sitemaps': sitemaps, 'template_name': 'sitemap_index.xml'}),
        url(r'^sitemap-(?P<section>.+)\.xml$', views.sitemap, {'sitemaps': sitemaps, 'template_name': 'sitemaps.xml'})
    )

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
