# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sections', '0002_section_max_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='enrollment',
            field=models.IntegerField(default=0),
        ),
    ]
