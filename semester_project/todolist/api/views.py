from time import sleep
from django.db.models import F
from django.shortcuts import render

# Create your views here.
from django.utils.datastructures import MultiValueDict
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from main_app.models import Task, Project, Label
from main_app.serializers import TaskSerializer, ProjectSerializer, LabelSerializer


# class TaskMixin(object):
#     """
#     Mixin to inherit from.
#     Here we're setting the query set and the serializer
#     """
#     queryset = Task.objects.filter()
#     serializer_class = TaskSerializer
#
#
# class TaskList(TaskMixin, ListCreateAPIView):
#     """
#     Return a list of all the tasks, or
#     create new ones
#     """
#     pass
#
#
# class TaskDetail(TaskMixin, RetrieveUpdateDestroyAPIView):
#     """
#     Return a specific task, update it, or delete it.
#     """
#     pass
#
#
# class ProjectMixin(object):
#     """
#     Mixin to inherit from.
#     Here we're setting the query set and the serializer
#     """
#     queryset = Project.objects.filter(owners__in=[request.user.id])
#     serializer_class = ProjectSerializer
#
#
# class ProjectList(ProjectMixin, ListCreateAPIView):
#     """
#     Return a list of all the tasks, or
#     create new ones
#     """
#     pass
#
#
# class ProjectDetail(ProjectMixin, RetrieveUpdateDestroyAPIView):
#     """
#     Return a specific task, update it, or delete it.
#     """
#     pass


@api_view(['GET', 'POST'])
def project_list(request):
    """
    List all projects, or create a new project.
    """
    if request.method == 'GET':
        projects = Project.objects.filter(owner=request.user)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        my_data = request.DATA
        my_data['owner'] = request.user.id
        serializer = ProjectSerializer(data=my_data)
        # serializer.owner = request.user
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def project_detail(request, pk):
    """
    Get, update, or delete a specific project
    """
    try:
        project = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProjectSerializer(project, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def task_list(request):
    """
    List all tasks, or create a new task.
    """
    if request.method == 'GET':
        tasks = Task.objects.filter(project__owner=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            if not request.session.has_key('ADDED_NEW_TASKS'):
                request.session['ADDED_NEW_TASKS'] = 0
            request.session['ADDED_NEW_TASKS'] += 1

            # request.user.
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def task_detail(request, pk):
    """
    Get, udpate, or delete a specific task
    """
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TaskSerializer(task, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def label_list(request):
    """
    List all labels, or create a new label.
    """
    if request.method == 'GET':
        labels = Label.objects.filter(user=request.user)
        serializer = LabelSerializer(labels, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        my_data = request.DATA
        my_data['user'] = request.user.id
        serializer = LabelSerializer(data=my_data)
        # serializer.owner = request.user
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def label_detail(request, pk):
    """
    Get, udpate, or delete a specific label
    """
    try:
        label = Label.objects.raw('SELECT * FROM main_app_label WHERE id = %s', [pk])[0]
        print(label)
    except Label.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = LabelSerializer(label)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = LabelSerializer(label, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        label.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def task_list_with_specific_title(request):
    """
    List all tasks where title equals project name.
    """
    if request.method == 'GET':
        tasks = Task.objects.filter(project__owner=request.user, title=F('project__name'))
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)