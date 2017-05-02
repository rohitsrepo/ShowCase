# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interpretations', '0005_interpretation_is_draft'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interpretation',
            name='is_draft',
            field=models.BooleanField(default=True),
        ),
    ]
