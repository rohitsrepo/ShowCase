# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buckets', '0003_bucket_watchers'),
    ]

    operations = [
        migrations.AddField(
            model_name='bucketmembership',
            name='description',
            field=models.CharField(default='', max_length=111, blank=True),
            preserve_default=False,
        ),
    ]
