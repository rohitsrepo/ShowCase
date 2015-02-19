from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', TemplateView.as_view(template_name='reader.html')),
                       url(r'^composition$', TemplateView.as_view(template_name='composition.html')),
                       url(r'^users', include('accounts.urls')),
                       url(r'^compositions', include('compositions.urls')),
                       url(r'^feed', include('feed.urls')),
		       )

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
