# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.contenttypes.management import update_all_contenttypes
from django.db import models, migrations
from django.conf import settings

def get_old_bookmarks(apps, schema_editor):
    update_all_contenttypes()
    BookMark = apps.get_model("bookmarks", "BookMark")
    User = apps.get_model("accounts", "User")
    ContentType = apps.get_model("contenttypes", "ContentType")
    ctype = ContentType.objects.get(app_label='compositions', model='composition')

    for user in User.objects.all():
        for bookmark in user.bookmarks.all():
            new_bookmark = BookMark.objects.create(
                owner = user,
                bookmark_type='AR',
                content_type = ctype,
                object_id=bookmark.id)



class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
        ('accounts', '0011_user_nsfw'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookMark',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('bookmark_type', models.CharField(max_length=2, choices=[(b'BK', b'bucket'), (b'AR', b'art')])),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RunPython(get_old_bookmarks)
    ]
