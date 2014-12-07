# Class based API views
from django.conf.urls import patterns, url
from api.views import TaskList, TaskDetail, ProjectList, ProjectDetail

urlpatterns = patterns('',

    # Regular URLs
	# url(r'^tasks/$', task_list, name='task_list'),
    # url(r'^tasks/(?P<pk>[0-9]+)$', task_detail, name='task_detail'),

    # Class based URLs,
    url( r'^tasks/$', TaskList.as_view(), name = 'task_list' ),
    url( r'^tasks/(?P<pk>[0-9]+)$', TaskDetail.as_view(), name = 'task_detail' ),

    url( r'^projects/$', ProjectList.as_view(), name = 'project_list' ),
    url( r'^projects/(?P<pk>[0-9]+)$', ProjectDetail.as_view(), name = 'project_detail' ),
)