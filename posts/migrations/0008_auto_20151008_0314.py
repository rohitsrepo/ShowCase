# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_auto_20151008_0256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_type',
            field=models.CharField(max_length=2, choices=[(b'IN', b'interpret'), (b'AD', b'add'), (b'CR', b'create'), (b'BK', b'bucket'), (b'MA', b'admire_art'), (b'MB', b'admire_bucket')]),
        ),
    ]
