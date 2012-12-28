# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Employee'
        db.create_table('holiTrack_employee', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('empId', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('startDate', self.gf('django.db.models.fields.DateField')()),
            ('leave_type', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal('holiTrack', ['Employee'])


    def backwards(self, orm):
        # Deleting model 'Employee'
        db.delete_table('holiTrack_employee')


    models = {
        'holiTrack.employee': {
            'Meta': {'object_name': 'Employee'},
            'empId': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'leave_type': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'startDate': ('django.db.models.fields.DateField', [], {})
        }
    }

    complete_apps = ['holiTrack']