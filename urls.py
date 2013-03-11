from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'newsissue.views.home', name='home'),
    # url(r'^newsissue/', include('newsissue.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^', include('newsissue.news.urls')),
)

if settings.DEBUG:
    from os.path import abspath, dirname, join
    PROJECT_DIR = dirname(abspath(__file__))
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': join(PROJECT_DIR, 'media')}),
    )