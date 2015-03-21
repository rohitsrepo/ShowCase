# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import accounts.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='picture',
            field=models.ImageField(default=b'/static/images/user_default.jpg', upload_to=accounts.models.get_upload_file_name_users),
            preserve_default=True,
        ),
    ]
