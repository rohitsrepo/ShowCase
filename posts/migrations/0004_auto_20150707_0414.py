# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def create_votes(apps, schema_editor):
    Post = apps.get_model("posts", "Post")
    PostVote = apps.get_model("postVotes", "PostVote")
    for post in Post.objects.all():
        vote = PostVote(positive=0, negative=0, post=post)
        vote.save()

class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20150707_0413'),
        ('postVotes', '0001_initial'),
    ]

    operations = [
    	migrations.RunPython(create_votes),
    ]
