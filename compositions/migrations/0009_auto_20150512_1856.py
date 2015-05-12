# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('compositions', '0008_auto_20150508_2106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='composition',
            name='slug',
            field=models.SlugField(unique=True, max_length=200),
        ),
    ]
