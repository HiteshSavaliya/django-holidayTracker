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
		if change == False:
			self.save_new_model(request, obj, form)
		else:
			self.update_existing_model(request, obj, form)
		
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
		obj.save()
		
	def update_existing_model(self,request,obj,form):
		print "Update_Existing_model"
		
		appliedLeave = request.POST['leave']
# 		Make sure applying leave is less than total allowed
#		print 'value of remaining' + repr(obj.remainingLeave)
		
#		print "from request Object"
#		print obj.total
#		print obj.leave
#		print obj.remainingLeave
		
#		Find the object
		e = Employee.objects.get(name=obj)
		
		if e is not None:
#			print "Old Object to be changed" + repr(e)
#			print e.total
#			print e.leave
#			print e.remainingLeave
			if e.remainingLeave == e.total and Decimal(appliedLeave) < 0.0:
				print 'This is not acceptable'
			else:
				newAppliedLeave = Decimal(appliedLeave ) + Decimal(e.leave)
				newRemainingLeave = Decimal(e.remainingLeave) - Decimal(appliedLeave) 
				newTotal = Decimal(newAppliedLeave) + Decimal(newRemainingLeave)
		
	#			print "New values"
	#			print Decimal(newTotal)
	#			print Decimal(newAppliedLeave)
	#			print Decimal(newRemainingLeave)
	
				
				if Decimal(newTotal) == Decimal(e.total) or Decimal(obj.total):
					if Decimal(newRemainingLeave) >= Decimal(0.0):
						print 'value of new remaining' + repr(newRemainingLeave)
						obj.remainingLeave = Decimal(newRemainingLeave)
						obj.leave = Decimal(newAppliedLeave)
						obj.save()
				else:
					print 'there is pro'
			
admin.site.register(Employee,EmployeeAdmin)