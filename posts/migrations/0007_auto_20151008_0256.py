# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_auto_20150822_1941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='composition',
            field=models.ForeignKey(related_name=b'posts', blank=True, to='compositions.Composition', null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_type',
            field=models.CharField(max_length=2, choices=[(b'IN', b'interpret'), (b'AD', b'add'), (b'CR', b'create'), (b'BK', b'bucket'), (b'AM', b'admire')]),
        ),
    ]
