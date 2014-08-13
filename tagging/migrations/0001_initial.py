# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tag'
        db.create_table(u'tagging_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag_name', self.gf('django.db.models.fields.CharField')(default='ART', max_length=26)),
            ('tag_def', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'tagging', ['Tag'])


    def backwards(self, orm):
        # Deleting model 'Tag'
        db.delete_table(u'tagging_tag')


    models = {
        u'tagging.tag': {
            'Meta': {'ordering': "('tag_name',)", 'object_name': 'Tag'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag_def': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'tag_name': ('django.db.models.fields.CharField', [], {'default': "'ART'", 'max_length': '26'})
        }
    }

    complete_apps = ['tagging']