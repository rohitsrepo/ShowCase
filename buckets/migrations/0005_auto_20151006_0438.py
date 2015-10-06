# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buckets', '0004_bucketmembership_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bucketmembership',
            name='description',
            field=models.CharField(max_length=111, null=True, blank=True),
        ),
    ]
