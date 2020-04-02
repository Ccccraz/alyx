# Generated by Django 2.2.6 on 2020-04-02 13:40

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BrainRegion',
            fields=[
                ('acronym', models.CharField(max_length=64, unique=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='experiments.BrainRegion')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='probeinsertion',
            name='model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='probe_insertion', to='experiments.ProbeModel'),
        ),
        migrations.AlterField(
            model_name='probeinsertion',
            name='session',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='probe_insertion', to='actions.EphysSession'),
        ),
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, help_text='Long name', max_length=255)),
                ('json', django.contrib.postgres.fields.jsonb.JSONField(blank=True, help_text='Structured data, formatted in a user-defined way', null=True)),
                ('axial', models.FloatField(blank=True, help_text='Distance in micrometers along the probe from the tip. 0 means the tip.', null=True)),
                ('lateral', models.FloatField(blank=True, help_text='Distance in micrometers accross the probe', null=True)),
                ('x', models.FloatField(blank=True, help_text='brain surface medio-lateral coordinate (um) ofthe insertion, right +, relative to Bregma', null=True, verbose_name='x-ml (um)')),
                ('y', models.FloatField(blank=True, help_text='brain surface antero-posterior coordinate (um) of the insertion, front +, relative to Bregma', null=True, verbose_name='y-ap (um)')),
                ('z', models.FloatField(blank=True, help_text='brain surface dorso-ventral coordinate (um) of the insertion, up +, relative to Bregma', null=True, verbose_name='z-dv (um)')),
                ('brain_region', models.ForeignKey(blank=True, default=0, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='channels', to='experiments.BrainRegion')),
                ('trajectory_estimate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='channels', to='experiments.TrajectoryEstimate')),
            ],
        ),
        migrations.AddConstraint(
            model_name='channel',
            constraint=models.UniqueConstraint(fields=('axial', 'lateral', 'trajectory_estimate'), name='unique_axial_lateral_trajectory_estimate'),
        ),
    ]