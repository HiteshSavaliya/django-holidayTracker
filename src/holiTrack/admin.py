from holiTrack.models import Employee, ApprovedLeaveHistory
from decimal import Decimal
from django.contrib import admin
from django.shortcuts import get_object_or_404
import logging
from datetime import timedelta
import datetime
from dateutil import rrule
from django.core.mail import send_mail
import smtplib

from ics import icsParser

logger = logging.getLogger(__name__)

class ApprovedLeaveHistoryInline(admin.TabularInline):
	model = ApprovedLeaveHistory
	can_delete = False #This will prevent history from deletion
	readonly_fields = ('leave_start_date', 'leave_end_date','leave_count','leave_type')
	fieldsets = (
		('History', {
            'classes': ('collapse',),
            'fields': ('leave_start_date', 'leave_end_date','leave_count','leave_type')
        }),
    )

class EmployeeAdmin(admin.ModelAdmin):
#	fieldsets = [
#	('Employee Details', {'fields': ['name','empId']}),
#	('Joining Date', {'fields': ['startDate']}),
#	('Leave type', {'fields' : ['leave_type']})
#	]
	list_display = ('name','email','remainingLeave','leave','total')
	readonly_fields = ('remainingLeave','total','leave','calenderYear')
	search_fields = ['name']
#	exclude = ('calenderYear',)
	
	fieldsets = (
		('Personal Details', {
            'fields': list_display
        }),
		('Leave Details',{
				'fields':('leaveFrom','leaveTo','leave_type')
			}),
        ('Options', {
            'classes': ('collapse',),
            'fields': ('calenderYear', 'startDate')
        }),
    )
	inlines = [ApprovedLeaveHistoryInline]
	publicHolidayParser = icsParser()
	publicHolidayParser.parse()
	
	def change_view(self, request, object_id, form_url='', extra_context=None):
		print 'Change_view called'
		print 'ExtraContext ', extra_context
		extra_context = extra_context or {}
		extra_context['Save_and_add_another'] = False
		extra_context['show_save_as_new'] = False
		return super(EmployeeAdmin, self).change_view(request, object_id, form_url=form_url, extra_context=extra_context)
	
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

				#Update leave history (it can include Sick,Vacation,business trip, etc)
				startDate = obj.leaveFrom
				endDate = obj.leaveTo
				leave_id = len(e.approvedleavehistory_set.all()) + 1 #counter
				e.approvedleavehistory_set.create(leaveId=leave_id,leave_start_date=startDate,leave_end_date=endDate,leave_count=appliedLeave,leave_type=obj.leave_type)
				e.save()

				# Update actual leave if it's vacation.
				if int(obj.leave_type) in (2,): #Vacation in LEAVE_TYPES_CHOICES
					print 'Leave type : %s' % (obj.get_leave_type_display())
					obj.remainingLeave = Decimal(newRemainingLeave)
					obj.leave = Decimal(newAppliedLeave)
				obj.save()
				
				# send mail to employee
				subject_Message =  "Your leave request update"

				body_Message =  """Hello %s,\n\nYour leave request of type %s starting from %s to %s is approved.\n\nFollowing is detail of your leave: \n\nLeave type: %s\nLeave starting date: %s\nLeave ending date: %s\nTotal leave applied: %d\nRemaining leave: %d\n\n\nThanks,\nRegards,\nHR Apptivation
				""" % (e.name,obj.get_leave_type_display(),startDate,endDate,obj.get_leave_type_display(),startDate,endDate,appliedLeave,obj.remainingLeave)
				try:
					if e.email is not None:
						send_mail(subject_Message, body_Message, 'hitesh.savaliya@gmail.com',[e.email], fail_silently=False)
				except (smtplib.SMTPException):
					self.message_user(request, "Email couldn't be sent to %s" % e.email)
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
		
		if fromDate is None or toDate is None:
			return

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