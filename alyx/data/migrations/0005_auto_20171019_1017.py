# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-19 09:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('imaging', '0004_auto_20171019_1017'),
        ('data', '0004_auto_20171019_1017'),
        ('electrophysiology', '0004_auto_20171019_1017'),
        ('behavior', '0004_auto_20171019_1017'),
    ]

    operations = [
        migrations.DeleteModel(
            name='EventSeries',
        ),
        migrations.DeleteModel(
            name='IntervalSeries',
        ),
        migrations.DeleteModel(
            name='TimeSeries',
        ),
        migrations.AddField(
            model_name='dataset',
            name='data_format',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='data.DataFormat'),
        ),
    ]
