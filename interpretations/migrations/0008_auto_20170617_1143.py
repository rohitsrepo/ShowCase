# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('interpretations', '0007_interpretation_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='interpretation',
            name='updated',
            field=models.DateTimeField(default=datetime.date(2017, 6, 17), auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='interpretation',
            name='user',
            field=models.ForeignKey(related_name=b'interprets', to=settings.AUTH_USER_MODEL),
        ),
    ]
