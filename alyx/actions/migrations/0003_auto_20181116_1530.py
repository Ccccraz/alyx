# Generated by Django 2.1.2 on 2018-11-16 15:30

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('actions', '0002_auto_20181015_0914'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taskprotocol',
            name='lab',
        ),
        migrations.RemoveField(
            model_name='taskprotocol',
            name='location',
        ),
        migrations.RemoveField(
            model_name='taskprotocol',
            name='procedures',
        ),
        migrations.RemoveField(
            model_name='taskprotocol',
            name='subject',
        ),
        migrations.RemoveField(
            model_name='taskprotocol',
            name='users',
        ),
        migrations.RemoveField(
            model_name='waterrestriction',
            name='adlib_drink',
        ),
        migrations.AddField(
            model_name='wateradministration',
            name='adlib',
            field=models.BooleanField(default=False),
        ),
        migrations.RemoveField(
            model_name='session',
            name='task_protocol',
        ),
        migrations.AddField(
            model_name='session',
            name='task_protocol',
            field=models.CharField(blank=True, default='', max_length=1023),
        ),
        migrations.AlterField(
            model_name='wateradministration',
            name='session',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='wateradmin_session_related', to='actions.Session'),
        ),
        migrations.AlterField(
            model_name='wateradministration',
            name='water_administered',
            field=models.FloatField(help_text='Water administered, in milliliters', blank=True, null=True, validators=[django.core.validators.MinValueValidator(limit_value=0)]),
        ),
        migrations.DeleteModel(
            name='TaskProtocol',
        ),
    ]
