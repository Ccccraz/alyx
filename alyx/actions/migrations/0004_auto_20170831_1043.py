# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-31 09:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actions', '0003_auto_20170821_0923'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='number',
            field=models.IntegerField(blank=True, help_text='Optional session number for this level', null=True),
        ),
        migrations.AddField(
            model_name='session',
            name='type',
            field=models.CharField(blank=True, help_text='User-defined session type (e.g. Base, Experiment)', max_length=255, null=True),
        ),
    ]
