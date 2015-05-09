# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('compositions', '0007_remove_composition_artist'),
    ]

    operations = [
        migrations.RenameField(
            model_name='composition',
            old_name='artist_new',
            new_name='artist',
        ),
    ]
