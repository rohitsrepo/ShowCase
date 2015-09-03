# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import compositions.models


class Migration(migrations.Migration):

    dependencies = [
        ('compositions', '0014_auto_20150702_2100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='composition',
            name='matter',
            field=models.ImageField(max_length=500, upload_to=compositions.models.get_upload_file_name_composition),
        ),
    ]
