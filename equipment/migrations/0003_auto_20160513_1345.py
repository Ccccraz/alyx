# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-05-13 13:45
from __future__ import unicode_literals

import datetime
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('equipment', '0002_daq_pipettepuller'),
    ]

    operations = [
        migrations.CreateModel(
            name='LightSource',
            fields=[
                ('appliance_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='equipment.Appliance')),
            ],
            options={
                'abstract': False,
            },
            bases=('equipment.appliance',),
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text="i.e. 'NeuroNexus'", max_length=255)),
                ('notes', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VirusBatch',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('virus_type', models.CharField(blank=True, help_text='UPenn ID or equivalent', max_length=255, null=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('date_time_made', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True)),
                ('nominal_titer', models.FloatField(blank=True, help_text='TODO: What unit?', null=True)),
            ],
            options={
                'verbose_name_plural': 'virus batches',
            },
        ),
        migrations.RenameModel(
            old_name='ExperimentLocation',
            new_name='LabLocation',
        ),
        migrations.RemoveField(
            model_name='cage',
            name='location',
        ),
        migrations.RemoveField(
            model_name='equipmentmanufacturer',
            name='id',
        ),
        migrations.RemoveField(
            model_name='equipmentmanufacturer',
            name='name',
        ),
        migrations.RemoveField(
            model_name='equipmentmanufacturer',
            name='notes',
        ),
        migrations.AlterField(
            model_name='extracellularprobe',
            name='prb',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, help_text='A JSON string describing the probe connectivity and geometry. For details, see https://github.com/klusta-team/kwiklib/wiki/Kwik-format#prb', null=True),
        ),
        migrations.CreateModel(
            name='VirusSource',
            fields=[
                ('supplier_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='equipment.Supplier')),
            ],
            options={
                'abstract': False,
            },
            bases=('equipment.supplier',),
        ),
        migrations.DeleteModel(
            name='Cage',
        ),
        migrations.AddField(
            model_name='supplier',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_equipment.supplier_set+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='equipmentmanufacturer',
            name='supplier_ptr',
            field=models.OneToOneField(auto_created=True, default='123e4567-e89b-12d3-a456-426655440000', on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='equipment.Supplier'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='virusbatch',
            name='virus_source',
            field=models.ForeignKey(blank=True, help_text='Who supplied the virus', null=True, on_delete=django.db.models.deletion.CASCADE, to='equipment.VirusSource'),
        ),
    ]
