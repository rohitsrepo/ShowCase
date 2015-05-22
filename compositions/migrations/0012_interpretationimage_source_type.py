# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('compositions', '0011_auto_20150519_0916'),
    ]

    operations = [
        migrations.AddField(
            model_name='interpretationimage',
            name='source_type',
            field=models.CharField(default=b'UPL', max_length=3, choices=[(b'UPL', b'upload'), (b'CRP', b'crop')]),
            preserve_default=True,
        ),
    ]
