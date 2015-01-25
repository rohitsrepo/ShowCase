# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('interpretations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('edited', models.BooleanField(default=False)),
                ('commenter', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('interpretation', models.ForeignKey(to='interpretations.Interpretation')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
