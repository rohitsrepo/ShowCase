# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_post_post_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_type',
            field=models.CharField(max_length=2, choices=[(b'IN', b'interpret'), (b'AD', b'add'), (b'CR', b'create'), (b'BK', b'bucket')]),
        ),
    ]
