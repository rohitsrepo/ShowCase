# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buckets', '0005_auto_20151006_0438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bucketmembership',
            name='description',
            field=models.TextField(max_length=200, blank=True),
        ),
    ]
