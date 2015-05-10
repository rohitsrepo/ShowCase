# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings

def add_artists(apps, schema_editor):
    User = apps.get_model('accounts', 'User')
    Composition = apps.get_model('compositions', 'Composition')

    for composition in Composition.objects.all():
        artist = composition.artist
        try:
            user = User.objects.get(first_name__exact=artist)
        except User.MultipleObjectsReturned:
            print "Assign first user for {0}".format(composition.title)
            user = User.objects.filter(first_name__exact=artist)[0]
        composition.artist_new = user
        composition.save()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('compositions', '0005_composition_artist'),
        ('accounts', '0005_user_is_artist')
    ]

    operations = [
        migrations.AddField(
            model_name='composition',
            name='artist_new',
            field=models.ForeignKey(related_name=b'arts', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.RunPython(add_artists)
    ]
