# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interpretations', '0004_interpretation_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='interpretation',
            name='is_draft',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
