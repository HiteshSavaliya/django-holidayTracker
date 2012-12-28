from holiTrack.models import Employee
from django.contrib import admin

class EmployeeAdmin(admin.ModelAdmin):
	fieldsets = [
	('Employee Details', {'fields': ['name','empId']}),
	('Joining Date', {'fields': ['startDate']}),
	('Leave type', {'fields' : ['leave_type']})
	]

admin.site.register(Employee,EmployeeAdmin)
