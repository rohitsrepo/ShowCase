# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('compositions', '0017_composition_added_with_bucket'),
    ]

    operations = [
        migrations.AddField(
            model_name='composition',
            name='major',
            field=models.CharField(default=b'#000000', max_length=7),
            preserve_default=True,
        ),
    ]
