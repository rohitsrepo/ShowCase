# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0002_fresh'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fresh',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
