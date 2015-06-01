# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('compositions', '0012_interpretationimage_source_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='composition',
            name='views',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
