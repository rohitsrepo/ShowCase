# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import buckets.models


class Migration(migrations.Migration):

    dependencies = [
        ('buckets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bucket',
            name='background',
            field=models.ImageField(null=True, upload_to=buckets.models.get_upload_file_name_background, blank=True),
            preserve_default=True,
        ),
    ]
