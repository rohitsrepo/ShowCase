# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20150410_0820'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_artist',
            field=models.BooleanField(default=False, help_text=b'Designate whether user is an artist.', verbose_name=b'artist status'),
            preserve_default=True,
        ),
    ]
