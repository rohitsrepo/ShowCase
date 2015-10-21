# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('follow', '0002_socialtracker_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socialtracker',
            name='access',
            field=models.ForeignKey(related_name=b'social_tracker', to='allaccess.AccountAccess'),
        ),
    ]
