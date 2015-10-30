# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('compositions', '0021_composition_matter_identifier'),
    ]

    operations = [
        migrations.AddField(
            model_name='composition',
            name='matter_format',
            field=models.CharField(default=b'', max_length=50),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='composition',
            name='matter_height',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='composition',
            name='matter_width',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='composition',
            name='matter_identifier',
            field=models.CharField(max_length=1000),
        ),
    ]
