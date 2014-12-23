from django.core import validators
from django.utils.datetime_safe import datetime
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from main_app.models import Task, Project, Label


class TaskSerializer( serializers.ModelSerializer ):

    t_date = serializers.DateTimeField(input_formats=('%d/%m/%Y', ), format='%d/%m/%Y', required=False, blank=True)

    class Meta:
        model = Task
        fields = ('id', 'title', 'isDone', 'project', 't_date', 'labels')


class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, required=False)
    # owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'name', 'owner', 'tasks')


class LabelSerializer( serializers.ModelSerializer ):

    class Meta:
        model = Label
        fields = ('id', 'title')