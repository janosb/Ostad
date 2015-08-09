# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sections', '0004_auto_20150723_0138'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassDetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=20)),
                ('subtitle', models.CharField(max_length=40)),
            ],
        ),
    ]
