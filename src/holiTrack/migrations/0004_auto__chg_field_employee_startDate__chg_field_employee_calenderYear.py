# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Employee.startDate'
        db.alter_column('holiTrack_employee', 'startDate', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'Employee.calenderYear'
        db.alter_column('holiTrack_employee', 'calenderYear', self.gf('django.db.models.fields.DateField')(null=True))

    def backwards(self, orm):

        # Changing field 'Employee.startDate'
        db.alter_column('holiTrack_employee', 'startDate', self.gf('django.db.models.fields.DateField')())

        # Changing field 'Employee.calenderYear'
        db.alter_column('holiTrack_employee', 'calenderYear', self.gf('django.db.models.fields.DateField')())

    models = {
        'holiTrack.employee': {
            'Meta': {'object_name': 'Employee'},
            'calenderYear': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'leave': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '5', 'decimal_places': '2'}),
            'leaveFrom': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'leaveTo': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'leave_type': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'remainingLeave': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'startDate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'total': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'})
        }
    }

    complete_apps = ['holiTrack']