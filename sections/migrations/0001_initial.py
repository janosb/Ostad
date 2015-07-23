# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('day_of_week', models.CharField(max_length=9)),
                ('time_string', models.CharField(max_length=20)),
                ('location', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('full_name', models.CharField(max_length=100)),
                ('email_address', models.CharField(max_length=100)),
                ('current_section', models.OneToOneField(to='sections.Section')),
            ],
        ),
    ]
