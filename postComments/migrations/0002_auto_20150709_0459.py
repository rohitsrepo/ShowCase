# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('postComments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postcomment',
            name='created',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='postcomment',
            name='post',
            field=models.ForeignKey(related_name=b'comments', to='posts.Post'),
        ),
    ]
