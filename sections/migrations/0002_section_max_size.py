# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sections', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='max_size',
            field=models.IntegerField(default=25),
            preserve_default=False,
        ),
    ]
