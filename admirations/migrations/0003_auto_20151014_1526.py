# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.contenttypes.management import update_all_contenttypes

from django.db import models, migrations


def create_migration_options(apps, schema_editor):
    update_all_contenttypes()
    AdmirationOption = apps.get_model("admirations", "AdmirationOption")

    options = ['',
        'Beautiful',
        'Unusual',
        'Thought-Provoking',
        'Repulsive',
        'Soothing',
        'Saddening',
        'Dark',
        'Touching',
        'Entertaining'
    ]

    for option in options:
        AdmirationOption.objects.create(word=option)

class Migration(migrations.Migration):

    dependencies = [
        ('admirations', '0002_admiration_word'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdmirationOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('word', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RunPython(create_migration_options),
    ]
