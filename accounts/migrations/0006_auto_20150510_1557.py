# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def delete_hollow_artists(apps, schema_editor):
    User = apps.get_model('accounts', 'User')

    for usr in User.objects.filter(is_active=False, is_artist=True):
    	if not usr.arts.all():
    		usr.delete()

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_user_is_artist'),
    ]

    operations = [
    	migrations.RunPython(delete_hollow_artists)
    ]
