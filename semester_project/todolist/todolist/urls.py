from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView
from main_app.views import LoginView, no_auth
from todolist import settings

urlpatterns = patterns('main_app.views',
    # Examples:
    url(r'^$', 'index', name='index'),
    url(r'^process/$', 'process', name='process'),
    url(r'^about/$', 'about', name='about'),
    url(r'^labels/$', 'labels', name='labels'),
    url(r'^filters/$', 'filters', name='filters'),
    url(r'^profile/$', 'profile', name='profile'),
    # url(r'^edit/$', 'edit_avatar', name='edit_avatar'),

    url(r'^signup/$', 'sign_up', name='sign_up'),
    # url(r'^signin/$', 'sign_in', name='sign_in'),
    url(r'^signin/$', no_auth(LoginView.as_view()), name='sign_in'),
    url(r'^signout/$', 'sign_out', name='sign_out'),
    url(
        r'^settings/',
        login_required(TemplateView.as_view(template_name="main_app/settings.html"), login_url=reverse_lazy('sign_in')),
        name="settings"
    ),
    url(
        r'^404/',
        TemplateView.as_view(template_name="main_app/404.html"),
        name="page_not_found"
    ),
    url(
        r'^help/',
        TemplateView.as_view(template_name="main_app/help.html"),
        name="help"
    ),
    url(
        r'^projects/',
        login_required(TemplateView.as_view(template_name="main_app/projects.html"), login_url=reverse_lazy('sign_in')),
        name="projects"
    ),

    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)', 'django.views.static.serve',
        { 'document_root': settings.MEDIA_ROOT }
    )
)