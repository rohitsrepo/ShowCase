# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('postVotes', '0002_auto_20150707_1821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postvotemembership',
            name='user',
            field=models.ForeignKey(related_name=b'vote_membership', to=settings.AUTH_USER_MODEL),
        ),
    ]
