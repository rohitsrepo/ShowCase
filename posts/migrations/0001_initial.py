# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('compositions', '0014_auto_20150702_2100'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField()),
                ('public', models.BooleanField(default=True)),
                ('object_id', models.PositiveIntegerField()),
                ('composition', models.ForeignKey(related_name=b'posts', to='compositions.Composition')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('creator', models.ForeignKey(related_name=b'user_posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
