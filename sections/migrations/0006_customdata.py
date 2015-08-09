# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sections', '0005_classdetails'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('full_name', models.CharField(max_length=100, verbose_name=b'Full name (first + last)')),
                ('email', models.EmailField(max_length=100, verbose_name=b'Email Address')),
                ('SID', models.IntegerField(verbose_name=b'Berkeley SID')),
                ('affiliation', models.CharField(max_length=100, verbose_name=b'Department/Affiliation')),
                ('full_time', models.BooleanField(max_length=20, verbose_name=b'Are you a full time student? (check this box if Yes)')),
                ('dob', models.DateField(max_length=20, verbose_name=b'Date of birth (mm/dd/yyyy)')),
                ('veteran', models.CharField(max_length=20, verbose_name=b'Are you a veteran or on active duty?')),
                ('tbi', models.CharField(max_length=20, verbose_name=b'Have you ever experienced a concussion, a traumatic brain injury, or a stroke?')),
                ('adhd', models.CharField(max_length=20, verbose_name=b'Have you been diagnosed with Attention Deficit, ADHD, or LD?')),
                ('meditation', models.CharField(max_length=40, verbose_name=b'Do you have experience meditating?')),
                ('video_games', models.CharField(max_length=40, verbose_name=b'Do you have experience playing video games?')),
                ('assessments', models.CharField(max_length=40, verbose_name=b'')),
            ],
        ),
    ]
