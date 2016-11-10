# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_mailoptions'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='picture_major',
            field=models.CharField(default=b'#000000', max_length=7),
            preserve_default=True,
        ),
    ]
