# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buckets', '0009_bucket_public'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bucket',
            name='public',
            field=models.BooleanField(default=False),
        ),
    ]
