# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag_name', models.CharField(default=b'ART', max_length=26, verbose_name=b'Tag name')),
                ('tag_def', models.CharField(max_length=200, verbose_name=b'Tag definition', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('tag_name',),
            },
            bases=(models.Model,),
        ),
    ]
