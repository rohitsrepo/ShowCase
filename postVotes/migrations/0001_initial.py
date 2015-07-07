# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PostVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('positive', models.PositiveIntegerField(default=0)),
                ('negative', models.PositiveIntegerField(default=0)),
                ('post', models.OneToOneField(related_name=b'vote', to='posts.Post')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PostVoteMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voteType', models.BooleanField(default=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('vote', models.ForeignKey(to='postVotes.PostVote')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='postvote',
            name='voters',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='postVotes.PostVoteMembership'),
            preserve_default=True,
        ),
    ]
