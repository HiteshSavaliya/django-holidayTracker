from holiTrack.models import Employee
from django.contrib import admin
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
#		logger.log(1, "Request %s",request)
#		logger.log(1, "obj %s",obj)
#		logger.log(1,"change %s", change)
		if change == False:
			self.save_new_model(request, obj, form)
		else:
			self.update_existing_model(request, obj, form)
		obj.save();
		
	def save_new_model(self,request,obj,form):
		logger.log(1, "")
		applyingLeave = request.POST['leave']
		applyingLeave = 0.0
		obj.leave = applyingLeave
		obj.remainingLeave = 20.0
		obj.total = 20.0
		
	def update_existing_model(self,request,obj,form):
		logger.log(1, "")
		
admin.site.register(Employee,EmployeeAdmin)