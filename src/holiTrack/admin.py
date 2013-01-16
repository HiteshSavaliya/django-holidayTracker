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
	list_display = ('name','startDate','leave_type')
	search_fields = ['name']
	
	def save_model(self,request,obj,form,change):
#		logger.log(1, "Request %s",request)
#		logger.log(1, "obj %s",obj)
#		logger.log(1,"change %s", change)
		e = request.POST['empId']
		if change == True:
			obj.empId = 5
		else:
			obj.empId = 10
		obj.save();

admin.site.register(Employee,EmployeeAdmin)