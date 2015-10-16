# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('compositions', '0016_composition_nsfw'),
    ]

    operations = [
        migrations.AddField(
            model_name='composition',
            name='added_with_bucket',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
