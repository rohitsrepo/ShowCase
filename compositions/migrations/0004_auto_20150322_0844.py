# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('compositions', '0003_auto_20150228_0952'),
    ]

    operations = [
        migrations.RenameField(
            model_name='composition',
            old_name='artist',
            new_name='uploader',
        ),
    ]
