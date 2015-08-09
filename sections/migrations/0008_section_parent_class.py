# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sections', '0007_auto_20150809_1941'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='parent_class',
            field=models.ForeignKey(default=1, to='sections.ClassDetails'),
            preserve_default=False,
        ),
    ]
