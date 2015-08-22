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
                      url(r'^$', 'accounts.clientViews.site_main', name='reader'),
                      url(r'^about-us$', TemplateView.as_view(template_name='aboutus.html'), name="about"),
                      url(r'^guidelines$', TemplateView.as_view(template_name='guidelines.html'), name='guidelines'),
                      url(r'^contact-us$', TemplateView.as_view(template_name='contactus.html'), name="contact"),
		       )

## Composition Urls
urlpatterns += patterns('',
                       url(r'^arts$', TemplateView.as_view(template_name='explore.html'), name='explore'),
                       url(r'^arts/(?P<slug>[\w-]+)$', 'compositions.clientViews.composition_main', name="composition-page"),
    )

## Account urls
urlpatterns += patterns('',
                       url(r'^register$', TemplateView.as_view(template_name='register.html'), name="register"),
                       url(r'^login/$', TemplateView.as_view(template_name='login.html'), name="login"),
                       url(r'^@(?P<slug>[\w-]+)', 'accounts.clientViews.artist_main', name="artist-page"),
                       url(r'^me/settings$', 'accounts.clientViews.user_settings', name="user-settings"),
                       # url(r'^me/collections$', 'accounts.clientViews.user_collections', name="user-collections"),
    )

## Interpretation Urls
urlpatterns += patterns('',
                       url(r'^arts/(?P<slug>[\w-]+)/add-interpretation$', 'compositions.clientViews.add_interpretation', name="interpretation-page"),
    )

## Post Urls
urlpatterns += patterns('',
                       url(r'^@(?P<user_slug>[\w-]+)/posts/(?P<post_id>[0-9]+)$', 'posts.clientViews.post_main'),
                       url(r'^posts$', 'streams.clientViews.posts_main', name='myposts'),
    )

# API urls
urlpatterns += patterns('',
                       url(r'^users', include('accounts.urls')),
                       url(r'^compositions', include('compositions.urls')),
                       url(r'^posts', include('posts.urls')),
                       url(r'^feeds', include('feeds.urls')),
                       url(r'^content', include('contentManager.urls')),
                       url(r'^buckets', include('buckets.urls')),
		       )

# Robots.txt
urlpatterns += patterns('',
                       url(r'^robots.txt$', TemplateView.as_view(template_name='robots.txt'), name='robots'),
    )

# SitesMap
from compositions.sitemaps import CompositionSitemap
from accounts.sitemaps import ArtistSitemap
from ShowCase.sitemaps import ReaderSitemap, StaticViewSitemap
from django.contrib.sitemaps import views

sitemaps = {
    'reader': ReaderSitemap,
    'compositions': CompositionSitemap,
    'artists': ArtistSitemap,
    'static': StaticViewSitemap
}

urlpatterns += patterns('',
        url(r'^sitemap\.xml$', views.index, {'sitemaps': sitemaps, 'template_name': 'sitemap_index.xml'}),
        url(r'^sitemap-(?P<section>.+)\.xml$', views.sitemap, {'sitemaps': sitemaps, 'template_name': 'sitemaps.xml'})
    )

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
