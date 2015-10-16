# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def create_migration_options(apps, schema_editor):
    AdmirationOption = apps.get_model("admirations", "AdmirationOption")

    options = ['Interesting', 'Inspiring']

    for option in options:
        AdmirationOption.objects.create(word=option)


class Migration(migrations.Migration):

    dependencies = [
        ('admirations', '0004_auto_20151014_1534'),
    ]

    operations = [
        migrations.RunPython(create_migration_options),
    ]
