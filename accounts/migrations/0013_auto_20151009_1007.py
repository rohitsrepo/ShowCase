# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def create_staff_user(apps, schema_editor):
    User = apps.get_model("accounts", "User")
    User.objects.create(name='ThirdDime Staff',
        email='info@thirddime.com')

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_remove_user_bookmarks'),
    ]

    operations = [
        migrations.RunPython(create_staff_user),
    ]
