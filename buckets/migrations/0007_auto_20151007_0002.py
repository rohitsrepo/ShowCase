# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buckets', '0006_auto_20151006_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bucketmembership',
            name='description',
            field=models.TextField(max_length=500, blank=True),
        ),
    ]
