# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interpretations', '0003_auto_20151210_1255'),
    ]

    operations = [
        migrations.AddField(
            model_name='interpretation',
            name='slug',
            field=models.SlugField(default=b'', max_length=200),
            preserve_default=True,
        ),
    ]
