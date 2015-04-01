# Class based API views
from django.conf.urls import patterns, url

# urlpatterns = patterns('',

    # Regular URLs
	# url(r'^tasks/$', task_list, name='task_list'),
    # url(r'^tasks/(?P<pk>[0-9]+)$', task_detail, name='task_detail'),

    # Class based URLs,
    # url( r'^tasks/$', TaskList.as_view(), name = 'task_list' ),
    # url( r'^tasks/(?P<pk>[0-9]+)$', TaskDetail.as_view(), name = 'task_detail' ),
    # 
    # url( r'^projects/$', project_list.as_view(), name = 'project_list' ),
    # url( r'^projects/(?P<pk>[0-9]+)$', ProjectDetail.as_view(), name = 'project_detail' ),
# )
from api.views import project_detail, project_list, task_list, task_detail, label_list, task_list_with_specific_title, \
    label_detail
# test

urlpatterns = patterns('',

    # Regular URLs
    url(r'^projects/$', project_list, name='project_list'),
    url(r'^projects/(?P<pk>[0-9]+)$', project_detail, name='project_detail'),

    url(r'^tasks/$', task_list, name='task_list'),
    url(r'^tasks/specific$', task_list_with_specific_title, name='task_list_with_specific_title'),
    url(r'^tasks/(?P<pk>[0-9]+)$', task_detail, name='task_detail'),

    url(r'^labels/$', label_list, name='label_list'),
    url(r'^labels/(?P<pk>\w+)$', label_detail, name='label_detail'),

    # Class based URLs,
    # url( r'^tasks/$', TaskList.as_view(), name = 'task_list' ),
    # url( r'^tasks/(?P<pk>[0-9]+)$', TaskDetail.as_view(), name = 'task_detail' ),
    # 
    # url( r'^projects/$', project_list.as_view(), name = 'project_list' ),
    # url( r'^projects/(?P<pk>[0-9]+)$', ProjectDetail.as_view(), name = 'project_detail' ),
)