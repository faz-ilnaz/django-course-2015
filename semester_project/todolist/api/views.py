from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from main_app.models import Task, Project
from main_app.serializers import TaskSerializer, ProjectSerializer


class TaskMixin(object):
    """
    Mixin to inherit from.
    Here we're setting the query set and the serializer
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskList(TaskMixin, ListCreateAPIView):
    """
    Return a list of all the tasks, or
    create new ones
    """
    pass


class TaskDetail(TaskMixin, RetrieveUpdateDestroyAPIView):
    """
    Return a specific task, update it, or delete it.
    """
    pass


class ProjectMixin(object):
    """
    Mixin to inherit from.
    Here we're setting the query set and the serializer
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectList(ProjectMixin, ListCreateAPIView):
    """
    Return a list of all the tasks, or
    create new ones
    """
    pass


class ProjectDetail(ProjectMixin, RetrieveUpdateDestroyAPIView):
    """
    Return a specific task, update it, or delete it.
    """
    pass