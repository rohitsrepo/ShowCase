# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings

def create_mail_options(apps, schema_editor):
    User = apps.get_model("accounts", "User")
    MailOptions = apps.get_model("accounts", "MailOptions")
    for user in User.objects.all():
        MailOptions.objects.create(user=user)

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_auto_20151009_1007'),
    ]

    operations = [
        migrations.CreateModel(
            name='MailOptions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('admiration', models.BooleanField(default=True)),
                ('to_bucket', models.BooleanField(default=True)),
                ('follow', models.BooleanField(default=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RunPython(create_mail_options),
    ]
