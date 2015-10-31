# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('compositions', '0022_auto_20151030_0619'),
    ]

    operations = [
        migrations.AddField(
            model_name='composition',
            name='matter_phash',
            field=models.CharField(default=b'', max_length=50),
            preserve_default=True,
        ),
    ]
