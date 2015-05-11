# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def add_name(apps, schema_editor):
    User = apps.get_model('accounts', 'User')

    for user in User.objects.all():
        full_name = ('%s %s' % (user.first_name, user.last_name)).title()
        user.name = full_name.strip()
        user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_user_is_artist'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(default='Init', max_length=80, verbose_name=b'first name'),
            preserve_default=False,
        ),
        migrations.RunPython(add_name)
    ]
