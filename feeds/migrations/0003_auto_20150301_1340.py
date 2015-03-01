# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0002_freshpost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freshpost',
            name='interpretation',
            field=models.ForeignKey(blank=True, to='interpretations.Interpretation', null=True),
            preserve_default=True,
        ),
    ]
