# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0004_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fresh',
            name='feed_type',
            field=models.CharField(max_length=2, choices=[(b'AR', b'art'), (b'BK', b'bucket'), (b'IN', b'interpret')]),
        ),
    ]
