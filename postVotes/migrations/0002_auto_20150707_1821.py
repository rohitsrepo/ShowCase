# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def update_votes(apps, schema_editor):
    Post = apps.get_model("posts", "Post")
    PostVote = apps.get_model("postVotes", "PostVote")
    PostVoteMembership = apps.get_model("postVotes", "PostVoteMembership")
    Interpretation = apps.get_model("interpretations", "Interpretation")
    InterpretationVote = apps.get_model("interpretationVotes", "InterpretationVote")
    VoteMembership = apps.get_model("interpretationVotes", "VoteMembership")
    for post in Post.objects.all():
    	interpretation = Interpretation.objects.get(pk=post.object_id)
    	interpretation_vote = InterpretationVote.objects.get(interpretation=interpretation)
        post_vote = PostVote.objects.get(post=post)

        post_vote.positive = interpretation_vote.positive
        post_vote.negative = interpretation_vote.negative
        post_vote.save()

        for membership in VoteMembership.objects.filter(vote=interpretation_vote):
        	PostVoteMembership.objects.create(user=membership.user, vote=post_vote, voteType=membership.voteType)

class Migration(migrations.Migration):

    dependencies = [
        ('postVotes', '0001_initial'),
        ('posts', '0004_auto_20150707_0414'),
        ('interpretations', '0002_interpretation_public'),
        ('interpretationVotes', '0001_initial'),
    ]

    operations = [
    	migrations.RunPython(update_votes),
    ]
