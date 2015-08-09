# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sections', '0009_auto_20150809_2119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='current_section',
            field=models.ForeignKey(to='sections.Section', null=True),
        ),
    ]
