# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('postComments', '0003_auto_20150709_0500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postcomment',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
