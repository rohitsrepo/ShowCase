# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admirations', '0003_auto_20151014_1526'),
    ]

    operations = [
        migrations.AddField(
            model_name='admiration',
            name='admire_as',
            field=models.ForeignKey(default=1, to='admirations.AdmirationOption'),
            preserve_default=False,
        ),
    ]
