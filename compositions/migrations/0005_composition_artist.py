# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('compositions', '0004_auto_20150322_0844'),
    ]

    operations = [
        migrations.AddField(
            model_name='composition',
            name='artist',
            field=models.CharField(default='Rohit', max_length=100, verbose_name=b'Artist'),
            preserve_default=False,
        ),
    ]
