from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from compositions import clientViews

admin.autodiscover()
favicon_view = RedirectView.as_view(url='/static/images/favicon.ico')

# WebClient urls
urlpatterns = patterns('',
                      url(r'^admin/', include(admin.site.urls)),
                      url(r'^$', 'accounts.clientViews.site_main', name='reader'),
                      url(r'^about-us$', TemplateView.as_view(template_name='aboutus.html'), name="about"),
                      url(r'^guidelines$', TemplateView.as_view(template_name='guidelines.html'), name='guidelines'),
                      url(r'^contact-us$', TemplateView.as_view(template_name='contactus.html'), name="contact"),
                      url(r'^find$', TemplateView.as_view(template_name='contactus.html'), name="contact"),
                      url(r'^favicon\.ico$', favicon_view),
		       )


# Search urls
urlpatterns += patterns('',
                      url(r'^search', TemplateView.as_view(template_name='search.html'), name="contact"),
               )

## Composition Urls
urlpatterns += patterns('',
                       url(r'^arts$', TemplateView.as_view(template_name='explore.html'), name='explore'),
                       url(r'^arts/(?P<slug>[\w-]+)$', 'compositions.clientViews.composition_main', name="composition-page"),
                       url(r'^arts/(?P<slug>[\w-]+)/series', 'compositions.clientViews.composition_series', name="composition-series"),
                       url(r'^contribute-art', 'compositions.clientViews.upload_artwork', name="composition-upload"),
    )

## Account urls
urlpatterns += patterns('',
                       url(r'^register$', 'accounts.clientViews.register_main', name="register"),
                       url(r'^login/$', 'accounts.clientViews.login_main', name="login"),
                       url(r'^reset-password$', TemplateView.as_view(template_name='reset-password.html'), name="password-reset"),
                       url(r'^reset-password-confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',  'accounts.clientViews.reset_password_confirm'),
                       url(r'^@(?P<user_slug>[\w-]+)/series/(?P<bucket_slug>[\w-]+)', 'buckets.clientViews.series_main', name="series-page"),
                       url(r'^@(?P<user_slug>[\w-]+)/tales/(?P<interpret_slug>[\w-]+)', 'interpretations.clientViews.show_interpretation', name="interpret-page"),
                       url(r'^@(?P<slug>[\w-]+)', 'accounts.clientViews.artist_main', name="artist-page"),
                       url(r'^me/settings$', 'accounts.clientViews.user_settings', name="user-settings"),
                       # url(r'^me/collections$', 'accounts.clientViews.user_collections', name="user-collections"),
    )

## Interpretation Urls
urlpatterns += patterns('',
                       url(r'^arts/(?P<slug>[\w-]+)/write-a-tale$', 'interpretations.clientViews.add_interpretation', name="interpretation-page"),
                       url(r'^write-a-tale/drafts/(?P<id>[0-9]+)$', 'interpretations.clientViews.edit_interpretation', {'mode': 'draft'}, name="draft-page"),
                       url(r'^write-a-tale/edit/(?P<id>[0-9]+)$', 'interpretations.clientViews.edit_interpretation', {'mode': 'edit'}, name="edit-page"),
    )

## Post Urls
urlpatterns += patterns('',
                       url(r'^@(?P<user_slug>[\w-]+)/posts/(?P<post_id>[0-9]+)$', 'posts.clientViews.post_main'),
                       url(r'^home$', 'streams.clientViews.posts_main', name='home'),
    )

# API urls
urlpatterns += patterns('',
                       url(r'^users', include('accounts.urls')),
                       url(r'^compositions', include('compositions.urls')),
                       url(r'^posts', include('posts.urls')),
                       url(r'^feeds', include('feeds.urls')),
                       url(r'^content', include('contentManager.urls')),
                       url(r'^buckets', include('buckets.urls')),
                       url(r'^bookmarks', include('bookmarks.urls')),
                       url(r'^admirations', include('admirations.urls')),
                       url(r'^interpretations', include('interpretations.urls')),
                       url(r'^api/search', include('search.urls')),
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
