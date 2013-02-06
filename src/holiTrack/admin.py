from holiTrack.models import Employee, ApprovedLeaveHistory
from decimal import Decimal
from django.contrib import admin
from django.shortcuts import get_object_or_404
import logging
from datetime import timedelta
import datetime
from dateutil import rrule

from ics import icsParser

logger = logging.getLogger(__name__)

class ApprovedLeaveHistoryInline(admin.TabularInline):
	model = ApprovedLeaveHistory
	can_delete = False #This will prevent history from deletion
	readonly_fields = ('leave_start_date', 'leave_end_date','leave_count')
	fieldsets = (
		('History', {
            'classes': ('collapse',),
            'fields': ('leave_start_date', 'leave_end_date','leave_count')
        }),
    )

class EmployeeAdmin(admin.ModelAdmin):
#	fieldsets = [
#	('Employee Details', {'fields': ['name','empId']}),
#	('Joining Date', {'fields': ['startDate']}),
#	('Leave type', {'fields' : ['leave_type']})
#	]
	list_display = ('name','remainingLeave','leave','total')
	readonly_fields = ('remainingLeave','total','leave','calenderYear')
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
	inlines = [ApprovedLeaveHistoryInline]
	publicHolidayParser = icsParser()
	publicHolidayParser.parse()
	
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

		total_days_in_current_year = (obj.calenderYear.replace(month=12,day=31) - obj.calenderYear).days 
		eligible_leave_count_per_day = 20.0/total_days_in_current_year
		
		total_number_of_days = self.no_of_days_from_start_to_end_date(obj)
		print 'No of days from start date to end of the year is:'
		print total_number_of_days

		obj.remainingLeave = total_number_of_days * eligible_leave_count_per_day
		obj.total = total_number_of_days * eligible_leave_count_per_day
		
#		calculate number of Weeks = From joining date to end of year
#		start_date = obj.startDate
#
##last day of the year
#		end_date = datetime.date(datetime.date.today().year,12,31)
#		total_weeks_in_current_year = self.no_of_weeks_from_start_to_end_date(start_date, end_date) 
#		print 'No of weeks from start date to end of the year is:'
#		print total_weeks_in_current_year
#		
#		eligible_leave_count_per_week = (20.0/52.0)
#		obj.remainingLeave = total_weeks_in_current_year * eligible_leave_count_per_week 
#		obj.total = obj.remainingLeave
		
		obj.save()
		
	def update_existing_model(self,request,obj,form):
		print "Update_Existing_model"
		
		appliedLeave = self.calculate_applying_leave_count(request,obj)
		if appliedLeave is None or appliedLeave == 0.0:
			self.message_user(request, "Re-check requested Date.Either 'End date smaller than begin date' or 'Applying leaves on weekend or public holiday'")
			return
		
# 		Make sure applying leave is less than total allowed
		print 'value of applied leave' + repr(appliedLeave)
		
#		Find the object
		e = get_object_or_404(Employee,id=obj.id)

		newAppliedLeave = Decimal(e.leave) + Decimal(appliedLeave)
		newRemainingLeave = 0.0
		
		print "New applied leave " + repr(newAppliedLeave)
		
		if Decimal(newAppliedLeave)  <= Decimal(e.total) and Decimal(newAppliedLeave) >= 0.0:
			newRemainingLeave = Decimal(e.total) - Decimal(newAppliedLeave)
			print "New applied Remaining " + repr(newRemainingLeave)
			if Decimal(newRemainingLeave) >= 0.0 and Decimal(newRemainingLeave) <= Decimal(e.total):
				obj.remainingLeave = Decimal(newRemainingLeave)
				obj.leave = Decimal(newAppliedLeave)
				
				#Update leave history
				startDate = obj.leaveFrom
				endDate = obj.leaveTo
				e.approvedleavehistory_set.create(leave_start_date=startDate,leave_end_date=endDate,leave_count=newAppliedLeave)
				e.save()
				
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
			if self.is_working_day(fromDate):
				return 1.0
		
		noOfDays = 0.0;
		if fromDate < toDate:
			oneday = timedelta(days=1)
			tmp = fromDate
			while tmp <= toDate:
				flag = self.is_working_day(tmp)
				if (flag):
					noOfDays +=1
				tmp += oneday
			return noOfDays
	#		return request.POST['leave']
		else:
			return None	

#	Returns true if given date is weekday and not public holiday
	def is_working_day(self,in_date):
		flag = False
		if not self.publicHolidayParser.is_holiday(in_date):
			flag = in_date.isoweekday() in (1,2,3,4,5)
		
		return flag
	
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
		
	def no_of_weeks_from_start_to_end_date(self,start_date,end_date):
		weeks = rrule.rrule(rrule.WEEKLY, dtstart=start_date, until=end_date)
		return weeks.count()
	
admin.site.register(Employee,EmployeeAdmin)
#admin.site.register(ApprovedLeaveHistory)