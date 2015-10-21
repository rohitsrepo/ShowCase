# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('allaccess', '0002_auto_20150511_1853'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialTracker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('remarks', models.TextField(blank=True)),
                ('access', models.ForeignKey(to='allaccess.AccountAccess')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
