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
                       url(r'^$', TemplateView.as_view(template_name='reader.html')),
                       url(r'^about-us$', TemplateView.as_view(template_name='aboutus.html')),
                       url(r'^guidelines$', TemplateView.as_view(template_name='guidelines.html')),
                       url(r'^contact-us$', TemplateView.as_view(template_name='contactus.html')),
                       url(r'^register$', TemplateView.as_view(template_name='register.html')),
                       url(r'^login$', TemplateView.as_view(template_name='login.html')),
                       url(r'^upload-art$', TemplateView.as_view(template_name='upload.html')),
                       url(r'^arts/(?P<slug>[\w-]+)$', 'compositions.clientViews.composition_main', name="composition-page"),
		       )

# API urls
urlpatterns += patterns('',
                       url(r'^users', include('accounts.urls')),
                       url(r'^compositions', include('compositions.urls')),
                       url(r'^feeds', include('feeds.urls')),
                       url(r'^content', include('contentManager.urls')),
		       )

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
