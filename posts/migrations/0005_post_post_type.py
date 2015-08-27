# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20150707_0414'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_type',
            field=models.CharField(default='IN', max_length=2, choices=[(b'IN', b'interpret'), (b'AD', b'add'), (b'CR', b'create')]),
            preserve_default=False,
        ),
    ]
