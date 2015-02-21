# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('compositions', '0002_composition_artist'),
        ('interpretations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaffPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('composition', models.ForeignKey(to='compositions.Composition')),
                ('interpretation', models.ForeignKey(to='interpretations.Interpretation')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
