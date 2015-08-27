# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import buckets.models


class Migration(migrations.Migration):

    dependencies = [
        ('compositions', '0014_auto_20150702_2100'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bucket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=25)),
                ('description', models.CharField(max_length=111, blank=True)),
                ('background', models.ImageField(null=True, upload_to=buckets.models.get_upload_file_name_background, blank=True)),
                ('slug', models.SlugField(unique=True, max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BucketMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('bucket', models.ForeignKey(related_name=b'membership', to='buckets.Bucket')),
                ('composition', models.ForeignKey(to='compositions.Composition')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='bucket',
            name='compositions',
            field=models.ManyToManyField(related_name=b'holders', through='buckets.BucketMembership', to='compositions.Composition'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bucket',
            name='owner',
            field=models.ForeignKey(related_name=b'buckets', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
