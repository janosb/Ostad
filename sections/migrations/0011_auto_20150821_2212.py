# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sections', '0010_auto_20150809_2128'),
    ]

    operations = [
        migrations.AddField(
            model_name='classdetails',
            name='admin_email',
            field=models.CharField(default=b'jbotyanszki@gmail.com', max_length=100),
        ),
        migrations.AddField(
            model_name='classdetails',
            name='admin_name',
            field=models.CharField(default=b'Janos Botyanszki', max_length=100),
        ),
    ]
