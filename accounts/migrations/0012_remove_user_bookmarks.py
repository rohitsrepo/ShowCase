# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_user_nsfw'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='bookmarks',
        ),
    ]
