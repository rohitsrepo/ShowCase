# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admirations', '0005_auto_20151016_0947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admiration',
            name='admire_type',
            field=models.CharField(max_length=2, choices=[(b'BK', b'bucket'), (b'AR', b'art'), (b'IN', b'interpret')]),
        ),
    ]
