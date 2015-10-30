# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.datetime_safe


class Migration(migrations.Migration):

    dependencies = [
        ('compositions', '0019_temporarycomposition'),
    ]

    operations = [
        migrations.AddField(
            model_name='temporarycomposition',
            name='modified',
            field=models.DateTimeField(default=django.utils.datetime_safe.datetime.now, auto_now=True),
            preserve_default=False,
        ),
    ]
