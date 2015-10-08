# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buckets', '0007_auto_20151007_0002'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bucket',
            name='watchers',
        ),
    ]
