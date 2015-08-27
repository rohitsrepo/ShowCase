# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20150725_2124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bookmarks',
            field=models.ManyToManyField(related_name=b'bookers', to=b'compositions.Composition'),
        ),
    ]
