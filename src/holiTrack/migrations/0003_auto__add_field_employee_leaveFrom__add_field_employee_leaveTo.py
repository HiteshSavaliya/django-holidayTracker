# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Employee.leaveFrom'
        db.add_column('holiTrack_employee', 'leaveFrom',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Employee.leaveTo'
        db.add_column('holiTrack_employee', 'leaveTo',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Employee.leaveFrom'
        db.delete_column('holiTrack_employee', 'leaveFrom')

        # Deleting field 'Employee.leaveTo'
        db.delete_column('holiTrack_employee', 'leaveTo')


    models = {
        'holiTrack.employee': {
            'Meta': {'object_name': 'Employee'},
            'calenderYear': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 21, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'leave': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'leaveFrom': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'leaveTo': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'leave_type': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'remainingLeave': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'startDate': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 21, 0, 0)'}),
            'total': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'})
        }
    }

    complete_apps = ['holiTrack']