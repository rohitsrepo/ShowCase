# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20150809_0028'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='nsfw',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
