# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buckets', '0008_remove_bucket_watchers'),
    ]

    operations = [
        migrations.AddField(
            model_name='bucket',
            name='public',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
