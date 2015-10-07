# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('bookmarks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmark',
            name='owner',
            field=models.ForeignKey(related_name=b'bookmarks', to=settings.AUTH_USER_MODEL),
        ),
    ]
