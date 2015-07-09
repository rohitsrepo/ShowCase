# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='interpretation',
            field=models.ForeignKey(related_name=b'comments', to='interpretations.Interpretation'),
        ),
    ]
