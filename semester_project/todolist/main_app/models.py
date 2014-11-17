from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields.related import ForeignKey, ManyToManyField, OneToOneField
import PIL


class Task(models.Model):
    title = models.CharField(max_length=300)
    t_date = models.DateTimeField()
    labels = ManyToManyField('Label', null=True)
    priority = ForeignKey('Priority', null=True)
    note = ForeignKey('Note', null=True)
    isActive = models.BooleanField(default=True)
    project = ForeignKey('Project', null=True)
    attachments = ManyToManyField('Attachment', null=True)

    def __str__(self):
        return ":".join([self.title, str(self.t_date)])



class Label(models.Model):
    title = models.CharField(max_length=50)
    color = models.ForeignKey('Dictionary')
    member = ForeignKey('Member')


class Project(models.Model):
    name = models.CharField(max_length=100)
    members = ManyToManyField('Member')
    color = models.ForeignKey('Dictionary', null=True)


class Note(models.Model):
    text = models.TextField()
    member = ForeignKey('Member')


class Attachment(models.Model):
    content = models.FileField()
    member = ForeignKey('Member')


class Filter(models.Model):
    text = models.TextField()
    member = ForeignKey('Member')


class Priority(models.Model):
    name = models.TextField()
    color = models.ForeignKey('Dictionary', null=True)
    value = models.PositiveSmallIntegerField()
    member = ForeignKey('Member')


class Dictionary(models.Model):
    parent = ForeignKey('self')
    value = models.TextField()


class Profile(models.Model):
    avatar = models.ImageField(upload_to='avatars', blank=True)
    birth_date = models.DateField(auto_now=True)
    registration_date = models.DateField(auto_now_add=True)


class Comment(models.Model):
    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    attachment = ManyToManyField('Attachment')
    task = ForeignKey('Task')
    member = ForeignKey('Member')


class Member(models.Model):
    user = OneToOneField(User)
    profile = OneToOneField('Profile')

