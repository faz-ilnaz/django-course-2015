# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_auto_20141109_0125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='attachments',
            field=models.ManyToManyField(to=b'main_app.Attachment', null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='labels',
            field=models.ManyToManyField(to=b'main_app.Label', null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.ForeignKey(to='main_app.Priority', null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='project',
            field=models.ForeignKey(to='main_app.Project', null=True),
        ),
    ]
