# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('buckets', '0002_bucket_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='bucket',
            name='watchers',
            field=models.ManyToManyField(related_name=b'watched_buckets', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
