# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def create_fresh_posts(apps, schema_editor):
    Fresh = apps.get_model("feeds", "Fresh")
    Composition = apps.get_model("compositions", "Composition")
    Bucket = apps.get_model("buckets", "Bucket")

    ContentType = apps.get_model("contenttypes", "ContentType")
    ctype_composition = ContentType.objects.get(app_label='compositions', model='composition')
    ctype_bucket = ContentType.objects.get(app_label='buckets', model='bucket')

    for composition in Composition.objects.all():
        post = Fresh()
        post.created = composition.created
        post.feed_type = 'AR'
        post.content_object = composition
        post.object_id = composition.id
        post.content_type = ctype_composition
        post.save()

    for bucket in Bucket.objects.all():
        post = Fresh()
        post.created = bucket.created
        post.feed_type = 'BK'
        post.object_id = bucket.id
        post.content_type = ctype_bucket
        post.content_object = bucket
        post.save()


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('feeds', '0001_initial'),
        ('compositions', '0016_composition_nsfw'),
        ('buckets', '0003_bucket_watchers')
    ]

    operations = [
        migrations.CreateModel(
            name='Fresh',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField()),
                ('public', models.BooleanField(default=True)),
                ('feed_type', models.CharField(max_length=2, choices=[(b'AR', b'art'), (b'BK', b'bucket')])),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RunPython(create_fresh_posts)
    ]
