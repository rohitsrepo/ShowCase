# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interpretations', '0002_interpretation_public'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interpretation',
            name='composition',
            field=models.ForeignKey(related_name=b'interprets', to='compositions.Composition'),
        ),
    ]
