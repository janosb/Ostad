# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sections', '0008_section_parent_class'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='parent_class',
            field=models.ForeignKey(default=0, to='sections.ClassDetails'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='student',
            unique_together=set([('full_name', 'parent_class')]),
        ),
    ]
