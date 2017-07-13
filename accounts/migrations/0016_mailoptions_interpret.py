# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_user_picture_major'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailoptions',
            name='interpret',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
