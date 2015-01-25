# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('compositions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='composition',
            name='artist',
            field=models.ForeignKey(related_name=b'compositions', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
