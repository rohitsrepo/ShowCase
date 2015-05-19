# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import compositions.models


class Migration(migrations.Migration):

    dependencies = [
        ('compositions', '0010_interpretationimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interpretationimage',
            name='image',
            field=models.ImageField(upload_to=compositions.models.get_upload_file_name_interpretation_image),
        ),
    ]
