from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'main_app.views.index', name='index'),
    url(r'^process/$', 'main_app.views.process', name='process'),
    url(r'^about/$', 'main_app.views.about', name='about'),
    url(r'^labels/$', 'main_app.views.labels', name='labels'),
    url(r'^filters/$', 'main_app.views.filters', name='filters'),
    url(r'^profile/$', 'main_app.views.profile', name='profile'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
