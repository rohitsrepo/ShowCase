# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookmarks', '0002_auto_20151007_0020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmark',
            name='bookmark_type',
            field=models.CharField(max_length=2, choices=[(b'BK', b'bucket'), (b'AR', b'art'), (b'IN', b'interpret')]),
        ),
    ]
