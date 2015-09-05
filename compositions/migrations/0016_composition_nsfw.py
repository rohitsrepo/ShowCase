# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('compositions', '0015_auto_20150903_0552'),
    ]

    operations = [
        migrations.AddField(
            model_name='composition',
            name='nsfw',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
