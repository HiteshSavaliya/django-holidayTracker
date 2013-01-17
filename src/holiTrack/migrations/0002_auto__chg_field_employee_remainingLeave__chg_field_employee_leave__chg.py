# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Employee.remainingLeave'
        db.alter_column('holiTrack_employee', 'remainingLeave', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2))

        # Changing field 'Employee.leave'
        db.alter_column('holiTrack_employee', 'leave', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2))

        # Changing field 'Employee.total'
        db.alter_column('holiTrack_employee', 'total', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2))

    def backwards(self, orm):

        # Changing field 'Employee.remainingLeave'
        db.alter_column('holiTrack_employee', 'remainingLeave', self.gf('django.db.models.fields.DecimalField')(max_digits=3, decimal_places=2))

        # Changing field 'Employee.leave'
        db.alter_column('holiTrack_employee', 'leave', self.gf('django.db.models.fields.DecimalField')(max_digits=3, decimal_places=2))

        # Changing field 'Employee.total'
        db.alter_column('holiTrack_employee', 'total', self.gf('django.db.models.fields.DecimalField')(max_digits=3, decimal_places=2))

    models = {
        'holiTrack.employee': {
            'Meta': {'object_name': 'Employee'},
            'calenderYear': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'leave': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'leave_type': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'remainingLeave': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'startDate': ('django.db.models.fields.DateField', [], {}),
            'total': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'})
        }
    }

    complete_apps = ['holiTrack']