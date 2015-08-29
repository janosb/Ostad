# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sections', '0011_auto_20150821_2212'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='section',
            name='enrollment',
        ),
    ]
