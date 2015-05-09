# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('compositions', '0006_composition_artist_new'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='composition',
            name='artist',
        ),
    ]
