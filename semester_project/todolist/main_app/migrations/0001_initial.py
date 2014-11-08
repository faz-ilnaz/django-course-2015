# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.FileField(upload_to=b'')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('comment_time', models.DateTimeField(auto_now_add=True)),
                ('attachment', models.ManyToManyField(to='main_app.Attachment')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Dictionary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.TextField()),
                ('parent', models.ForeignKey(to='main_app.Dictionary')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('color', models.ForeignKey(to='main_app.Dictionary')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('member', models.ForeignKey(to='main_app.Member')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Priority',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
                ('value', models.PositiveSmallIntegerField()),
                ('color', models.ForeignKey(to='main_app.Dictionary')),
                ('member', models.ForeignKey(to='main_app.Member')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('avatar', models.FileField(upload_to=b'')),
                ('birth_date', models.DateField()),
                ('registration_date', models.DateField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('members', models.ManyToManyField(to='main_app.Member')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=300)),
                ('t_date', models.DateTimeField()),
                ('isActive', models.BooleanField(default=True)),
                ('attachments', models.ManyToManyField(to='main_app.Attachment')),
                ('labels', models.ManyToManyField(to='main_app.Label')),
                ('note', models.ForeignKey(to='main_app.Note')),
                ('priority', models.ForeignKey(to='main_app.Priority')),
                ('project', models.ForeignKey(to='main_app.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='member',
            name='profile',
            field=models.OneToOneField(to='main_app.Profile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, unique=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='label',
            name='member',
            field=models.ForeignKey(to='main_app.Member'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='filter',
            name='member',
            field=models.ForeignKey(to='main_app.Member'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='member',
            field=models.ForeignKey(to='main_app.Member'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='task',
            field=models.ForeignKey(to='main_app.Task'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attachment',
            name='member',
            field=models.ForeignKey(to='main_app.Member'),
            preserve_default=True,
        ),
    ]
