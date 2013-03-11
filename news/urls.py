from django.conf.urls.defaults import *

urlpatterns = patterns('news.views',
    (r'^/?(category/(?P<category_id>[\w\-]+)/)?((?P<page>\d+)/)?$', 'list_view'),
    #(r'^/?((?P<page>\d+)/)?$', 'list_view'),
    (r'^entry/(?P<entry_id>\d+)/$', 'entry_view'),
    (r'^(?P<type>goodnews|badnews)/(?P<entry_id>\d+)/$', 'vote_view'),
)