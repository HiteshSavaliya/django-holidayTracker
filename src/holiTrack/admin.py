from holiTrack.models import Employee
from django.contrib import admin
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.core import exceptions
from django.template.context import RequestContext
from decimal import *
import logging
#from django.utils.datetime_safe import datetime,time
from datetime import datetime, time, timedelta
import datetime
from dateutil import rrule

logger = logging.getLogger(__name__)

class EmployeeAdmin(admin.ModelAdmin):
#	fieldsets = [
#	('Employee Details', {'fields': ['name','empId']}),
#	('Joining Date', {'fields': ['startDate']}),
#	('Leave type', {'fields' : ['leave_type']})
#	]
	list_display = ('name','remainingLeave','leave','total')
	readonly_fields = ('remainingLeave','total','leave')
	search_fields = ['name']
#	exclude = ('calenderYear',)
	
	fieldsets = (
		('Personal Details', {
            'fields': list_display
        }),
		('Leave Details',{
				'fields':('leaveFrom','leaveTo')
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
#		logger.log(1, "New model")
		print 'Save New Model'
#		applyingLeave = request.POST['leave']
#		New object is getting created. Set Apply leave to 0.
		applyingLeave = 0.0
		obj.leave = applyingLeave
		obj.calenderYear = datetime.date(datetime.date.today().year,1,1)
#		Remaining leave should be calculated based equation:

#		if startDate is greater than current year
#		noOfLeavesPerweek = 20.0/52
#		noOfLeavesPerMonth = 20.0/12
		total_days_in_current_year = (obj.calenderYear.replace(month=12,day=31) - obj.calenderYear).days 
		eligible_leave_count_per_day = 20.0/total_days_in_current_year
		
#		calculate number of Weeks = From joining date to end of year
#		calculate number of months =  from joining date to end of year
#		obj.Total = noOfMonths * noOfLeavesPerMonth 
		total_number_of_days = self.no_of_days_from_start_to_end_date(obj)
		print 'No of days from start date to end of the year is:'
		print total_number_of_days

		obj.remainingLeave = total_number_of_days * eligible_leave_count_per_day
		obj.total = total_number_of_days * eligible_leave_count_per_day
		obj.save()
		
	def update_existing_model(self,request,obj,form):
		print "Update_Existing_model"
		
		appliedLeave = self.calculate_applying_leave_count(request,obj)
		if appliedLeave is None:
			self.message_user(request, "End date smaller than begin date of holidays")
			return
		
# 		Make sure applying leave is less than total allowed
		print 'value of applied leave' + repr(appliedLeave)
		
#		print "from request Object"
#		print obj.total
#		print obj.leave
#		print obj.remainingLeave
		
#		Find the object
		e = get_object_or_404(Employee,id=obj.id)
#		e = Employee.objects.get(name=obj)

		newAppliedLeave = Decimal(e.leave) + Decimal(appliedLeave)
		newRemainingLeave = 0.0
		
		print "New applied leave " + repr(newAppliedLeave)
		
		if Decimal(newAppliedLeave)  <= Decimal(e.total) and Decimal(newAppliedLeave) >= 0.0:
			newRemainingLeave = Decimal(e.total) - Decimal(newAppliedLeave)
			print "New applied Remaining " + repr(newRemainingLeave)
			if Decimal(newRemainingLeave) >= 0.0 and Decimal(newRemainingLeave) <= Decimal(e.total):
				obj.remainingLeave = Decimal(newRemainingLeave)
				obj.leave = Decimal(newAppliedLeave)
				obj.save()
			else:
				print 'Not Valid NUMBER'
		else:
			print 'Not valid  number'
			self.message_user(request, "Value %s for Applying Leave is not valid" % appliedLeave)
#			return render_to_response('templates/500.html',{}) #,context_instance=RequestContext(request))	
			
	def calculate_applying_leave_count(self,request,obj):
#		fromDate = datetime.date(request.POST['leaveFrom'])
#		toDate = datetime.date(request.POST['leaveTo'])
		
		fromDate = obj.leaveFrom
		toDate = obj.leaveTo
		
		if fromDate == toDate:
			return 1.0
		
		noOfDays = 0.0;
		if fromDate < toDate:
			oneday = timedelta(days=1)
			tmp = fromDate
			while tmp <= toDate:
				flag = tmp.isoweekday() in (1,2,3,4,5)
				if (flag):
					noOfDays +=1
				tmp += oneday
			return noOfDays
	#		return request.POST['leave']
		else:
			return None	
	
	
	def no_of_days_from_start_to_end_date(self,obj):
		if obj.calenderYear == None:
			print 'calender year is None'
			return 0
			
		if obj.startDate == None:
			print 'start year is None'
			obj.startDate = obj.calenderYear
	
		lastDateOfCalenderYear = obj.calenderYear.replace(month=12,day=31)
#		print "Last day of the year" 
#		print lastDateOfCalenderYear.isoformat()
		return (lastDateOfCalenderYear - obj.startDate).days
		
	def no_of_weeks_from_start_to_end_date(self,obj):
		start_date = obj.startDate 
		end_date = datetime.date(obj.calenderYear.date.year,12,31)
		
		weeks = rrule.rrule(rrule.WEEKLY, dtstart=start_date, until=end_date)
		return weeks.count()
	
admin.site.register(Employee,EmployeeAdmin)