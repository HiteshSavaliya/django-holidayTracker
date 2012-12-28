# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Employee.leave_type'
        db.add_column('holiTrack_employee', 'leave_type',
                      self.gf('django.db.models.fields.CharField')(default=0, max_length=2),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Employee.leave_type'
        db.delete_column('holiTrack_employee', 'leave_type')


    models = {
        'holiTrack.employee': {
            'Meta': {'object_name': 'Employee'},
            'empId': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'leave_type': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'startDate': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['holiTrack']