# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interpretations', '0006_auto_20170422_1250'),
    ]

    operations = [
        migrations.AddField(
            model_name='interpretation',
            name='title',
            field=models.CharField(default='', max_length=140),
            preserve_default=False,
        ),
    ]
