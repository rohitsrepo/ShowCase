# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interpretations', '0008_auto_20170617_1143'),
    ]

    operations = [
        migrations.AddField(
            model_name='interpretation',
            name='post_id',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
