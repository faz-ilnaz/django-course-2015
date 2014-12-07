from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields.related import ForeignKey, ManyToManyField, OneToOneField
import PIL


class Task(models.Model):
    title = models.CharField(max_length=300)
    t_date = models.DateTimeField(auto_now_add=True, auto_now=True)
    labels = ManyToManyField('Label', null=True)
    priority = ForeignKey('Priority', null=True)
    note = ForeignKey('Note', null=True)
    isDone = models.BooleanField(default=True)
    project = ForeignKey('Project', null=True, related_name='tasks')
    attachments = ManyToManyField('Attachment', null=True)

    def to_dict(self):
        return {'id': self.pk, 'title': self.title}

    def __unicode__(self):
        return self.title[:50] + ' ' + unicode(self.project)

    def __str__(self):
        return ":".join([self.title, str(self.t_date)])


class Label(models.Model):
    title = models.CharField(max_length=50)
    color = models.ForeignKey('Dictionary')
    user = ForeignKey(User)


class Project(models.Model):
    name = models.CharField(max_length=100)
    owners = ManyToManyField(User, related_name='projects')
    color = models.ForeignKey('Dictionary', null=True)

    def __unicode__(self):
        return '"' + self.name + '" by ' + unicode(self.owners)

    def __str__(self):
        return ":".join([self.id.__str__(), self.name])


class Note(models.Model):
    text = models.TextField()
    user = ForeignKey(User)


class Attachment(models.Model):
    content = models.FileField()
    user = ForeignKey(User)


class Filter(models.Model):
    text = models.TextField()
    user = ForeignKey(User)


class Priority(models.Model):
    name = models.TextField()
    color = models.ForeignKey('Dictionary', null=True)
    value = models.PositiveSmallIntegerField()
    user = models.ForeignKey(User)


class Dictionary(models.Model):
    parent = ForeignKey('self')
    value = models.TextField()


class Profile(models.Model):
    user = OneToOneField(User)
    avatar = models.ImageField(upload_to='avatars', blank=True)
    birth_date = models.DateField(auto_now=True)
    registration_date = models.DateField(auto_now_add=True)


class Comment(models.Model):
    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    attachment = ManyToManyField('Attachment')
    task = ForeignKey('Task')
    user = ForeignKey(User)
