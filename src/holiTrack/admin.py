from holiTrack.models import Employee
from django.contrib import admin

class EmployeeAdmin(admin.ModelAdmin):
#	fieldsets = [
#	('Employee Details', {'fields': ['name','empId']}),
#	('Joining Date', {'fields': ['startDate']}),
#	('Leave type', {'fields' : ['leave_type']})
#	]
	list_display = ('name','startDate','leave_type')
	search_fields = ['name']

admin.site.register(Employee,EmployeeAdmin)