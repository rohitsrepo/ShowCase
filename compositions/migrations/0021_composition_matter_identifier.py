# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('compositions', '0020_temporarycomposition_modified'),
    ]

    operations = [
        migrations.AddField(
            model_name='composition',
            name='matter_identifier',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
