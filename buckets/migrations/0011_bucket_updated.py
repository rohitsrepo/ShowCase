# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('buckets', '0010_auto_20151016_1037'),
    ]

    operations = [
        migrations.AddField(
            model_name='bucket',
            name='updated',
            field=models.DateTimeField(default=datetime.date(2017, 6, 17), auto_now=True),
            preserve_default=False,
        ),
    ]
