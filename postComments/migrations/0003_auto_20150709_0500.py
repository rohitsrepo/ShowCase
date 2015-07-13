# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def update_comments(apps, schema_editor):
    Post = apps.get_model("posts", "Post")
    PostComment = apps.get_model("postComments", "PostComment")
    Interpretation = apps.get_model("interpretations", "Interpretation")

    for post in Post.objects.all():
    	interpretation = Interpretation.objects.get(pk=post.object_id)
    	interpretation_comments = interpretation.comments.all()

        for interpretation_comment in interpretation_comments:
            PostComment.objects.create(
                comment = interpretation_comment.comment,
                created = interpretation_comment.created,
                commenter = interpretation_comment.commenter,
                post = post)

class Migration(migrations.Migration):

    dependencies = [
        ('postComments', '0002_auto_20150709_0459'),
        ('posts', '0004_auto_20150707_0414'),
        ('interpretations', '0002_interpretation_public'),
        ('comments', '0002_auto_20150709_0459'),
    ]

    operations = [
    	migrations.RunPython(update_comments),
    ]
