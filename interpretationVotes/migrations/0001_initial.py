# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('interpretations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InterpretationVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('positive', models.PositiveIntegerField(default=0)),
                ('negative', models.PositiveIntegerField(default=0)),
                ('interpretation', models.OneToOneField(related_name=b'vote', to='interpretations.Interpretation')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VoteMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voteType', models.BooleanField(default=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('vote', models.ForeignKey(to='interpretationVotes.InterpretationVote')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='interpretationvote',
            name='voters',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='interpretationVotes.VoteMembership'),
            preserve_default=True,
        ),
    ]
