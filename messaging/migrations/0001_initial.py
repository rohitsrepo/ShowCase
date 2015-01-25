# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sender', models.EmailField(max_length=50, verbose_name=b'sender_email')),
                ('subject', models.CharField(max_length=100, verbose_name=b'subject')),
                ('body', models.TextField(max_length=500, verbose_name=b'body')),
                ('read', models.BooleanField(default=False, verbose_name=b'read')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('recipient', models.ForeignKey(related_name=b'messages', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('created',),
            },
            bases=(models.Model,),
        ),
    ]
