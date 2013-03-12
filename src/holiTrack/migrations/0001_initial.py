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
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=254, null=True)),
            ('calenderYear', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('startDate', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('remainingLeave', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('leave', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=5, decimal_places=2)),
            ('leaveFrom', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('leaveTo', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('total', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('leave_type', self.gf('django.db.models.fields.CharField')(default=0, max_length=2)),
        ))
        db.send_create_signal('holiTrack', ['Employee'])

        # Adding model 'ApprovedLeaveHistory'
        db.create_table('holiTrack_approvedleavehistory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('leaveId', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('leave_start_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('leave_end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('associated_with_employee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['holiTrack.Employee'])),
            ('leave_count', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=5, decimal_places=2)),
            ('leave_type', self.gf('django.db.models.fields.CharField')(default=0, max_length=2)),
        ))
        db.send_create_signal('holiTrack', ['ApprovedLeaveHistory'])


    def backwards(self, orm):
        # Deleting model 'Employee'
        db.delete_table('holiTrack_employee')

        # Deleting model 'ApprovedLeaveHistory'
        db.delete_table('holiTrack_approvedleavehistory')


    models = {
        'holiTrack.approvedleavehistory': {
            'Meta': {'object_name': 'ApprovedLeaveHistory'},
            'associated_with_employee': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['holiTrack.Employee']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'leaveId': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'leave_count': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '5', 'decimal_places': '2'}),
            'leave_end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'leave_start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'leave_type': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '2'})
        },
        'holiTrack.employee': {
            'Meta': {'object_name': 'Employee'},
            'calenderYear': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'leave': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '5', 'decimal_places': '2'}),
            'leaveFrom': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'leaveTo': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'leave_type': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'remainingLeave': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'startDate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'total': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'})
        }
    }

    complete_apps = ['holiTrack']