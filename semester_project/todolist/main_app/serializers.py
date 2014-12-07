from django.utils.datetime_safe import datetime
from rest_framework import serializers
from main_app.models import Task, Project


class TaskSerializer( serializers.ModelSerializer ):

    class Meta:
        model = Task
        fields = ('id', 'title', 'isDone', 'project', 't_date')


class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True)

    class Meta:
        model = Project
        fields = ('id', 'name', 'owners', 'tasks')