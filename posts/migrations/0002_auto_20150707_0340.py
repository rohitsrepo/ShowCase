# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.contenttypes.management import update_all_contenttypes
from django.db import models, migrations

def create_posts(apps, schema_editor):
    update_all_contenttypes()
    Post = apps.get_model("posts", "Post")
    Interpretation = apps.get_model("interpretations", "Interpretation")
    User = apps.get_model("accounts", "User")
    ContentType = apps.get_model("contenttypes", "ContentType")
    ctype = ContentType.objects.get(app_label='interpretations', model='interpretation')
    for interpretation in Interpretation.objects.all():
        post = Post()
        post.composition = interpretation.composition
        post.creator = User.objects.get(pk=interpretation.user.id)
        post.created = interpretation.created
        post.public = interpretation.public
        post.content_type = ctype
        post.object_id = interpretation.id
        post.content_object = interpretation
        post.save()

class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
        ('interpretations', '0002_interpretation_public'),
        ('postVotes', '0001_initial'),
        ('accounts', '0008_user_slug'),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
    	migrations.RunPython(create_posts),
    ]
