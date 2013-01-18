from holiTrack.models import Employee
from django.contrib import admin
from decimal import *
import logging

logger = logging.getLogger(__name__)

class EmployeeAdmin(admin.ModelAdmin):
#	fieldsets = [
#	('Employee Details', {'fields': ['name','empId']}),
#	('Joining Date', {'fields': ['startDate']}),
#	('Leave type', {'fields' : ['leave_type']})
#	]
	list_display = ('name','remainingLeave','leave','total')
	readonly_fields = ('remainingLeave','total')
	search_fields = ['name']
#	exclude = ('calenderYear',)
	
	fieldsets = (
		(None, {
            'fields': list_display
        }),
        ('Options', {
            'classes': ('collapse',),
            'fields': ('calenderYear', 'startDate')
        }),
    )
	
	def save_model(self,request,obj,form,change):
		print 'Save_model'
#		logger.log(1, "Request %s",request)
#		logger.log(1, "obj %s",obj)
#		logger.log(1,"change %s", change)
#		if change == False:
#			self.save_new_model(request, obj, form)
#		else:
		self.update_existing_model(request, obj, form)
		obj.save();
		
	def save_new_model(self,request,obj,form):
		logger.log(1, "New model")
#		applyingLeave = request.POST['leave']
#		New object is getting created. Set Apply leave to 0.
		applyingLeave = 0.0
		obj.leave = applyingLeave
#		Remaining leave should be calculated based equation:

#		if startDate is greater than current year
#		noOfLeavesPerweek = 20.0/52
#		noOfLeavesPerMonth = 20.0/12
#		calculate number of Weeks = From joining date to end of year
#		calculate number of months =  from joining date to end of year
#		obj.Total = noOfMonths * noOfLeavesPerMonth

		obj.remainingLeave = 20.0
		obj.total = 20.0
		
	def update_existing_model(self,request,obj,form):
		
		applyingLeave = request.POST['leave']
		print 'update ' + repr(applyingLeave)
# 		Make sure applying leave is less than total allowed
		print 'value of remaining' + repr(obj.remainingLeave)
		if Decimal(applyingLeave) < Decimal(obj.remainingLeave):
			tmp = Decimal(obj.remainingLeave) - Decimal(applyingLeave)
			print 'value of new remaining' + repr(tmp)
			if Decimal(tmp) >= 0.0:
				obj.remainingLeave = Decimal(tmp)
		else:
			print 'there is pro'
		obj.save();
		
admin.site.register(Employee,EmployeeAdmin)