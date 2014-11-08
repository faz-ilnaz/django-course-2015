# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='color',
            field=models.ForeignKey(to='main_app.Dictionary', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='priority',
            name='color',
            field=models.ForeignKey(to='main_app.Dictionary', null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='note',
            field=models.ForeignKey(to='main_app.Note', null=True),
        ),
    ]
