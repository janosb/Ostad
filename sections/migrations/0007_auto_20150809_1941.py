# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sections', '0006_customdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classdetails',
            name='subtitle',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='classdetails',
            name='title',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='customdata',
            name='adhd',
            field=models.CharField(max_length=40, verbose_name=b'Have you been diagnosed with Attention Deficit, ADHD, or LD?'),
        ),
        migrations.AlterField(
            model_name='customdata',
            name='dob',
            field=models.DateField(verbose_name=b'Date of birth (mm/dd/yyyy)'),
        ),
        migrations.AlterField(
            model_name='customdata',
            name='full_time',
            field=models.BooleanField(verbose_name=b'Are you a full time student? (check this box if Yes)'),
        ),
    ]
