from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'blog.views.index', name='index'),
    url(r'^new_post/$', 'blog.views.new_post', name='new_post'),
    url(r'^search/', 'blog.views.search', name='search'),


    url(r'^admin/', include(admin.site.urls)),
)





