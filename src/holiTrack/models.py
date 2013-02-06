from django.db import models

class Employee (models.Model):
    
    LEAVE_TYPES_CHOICES = (
        ('0', 'Working'),
        ('1', 'Sick'),
        ('2', 'Vacation'),
        ('3', 'Bank Holiday'),
        ('4', 'Business Trip'),
        ('5','Weekend'),
        ('6','Other'),
    )
    
    def __unicode__(self):
        return self.name;
    
    name = models.CharField(max_length=256)
#    empId = models.AutoField(primary_key=True)
    calenderYear = models.DateField('Calender Year',blank=True,null=True)
    startDate = models.DateField('Join Date',blank=True,null=True)
    remainingLeave = models.DecimalField('Remaining leave',max_digits=5,decimal_places=2)
    leave = models.DecimalField ('Applied leave',default=0.0,max_digits=5,decimal_places=2)
    leaveFrom = models.DateField ('From',blank=True,null=True)
    leaveTo = models.DateField ('To',blank=True,null=True)
    total = models.DecimalField(max_digits=5,decimal_places=2)
    leave_type = models.CharField(max_length=2, choices=LEAVE_TYPES_CHOICES)
    
#    def __init__(self,*args,**kwargs):
#        print "Employee __init__"
#        models.Model.__init__(self,*args,**kwargs)
#        self.calenderYear = datetime.date(datetime.date.today().year,1,1)
#        self.startDate = self.calenderYear


class ApprovedLeaveHistory(models.Model):
#    leaveId = models.AutoField()
    leave_start_date = models.DateField('Start Date')
    leave_end_date = models.DateField('End Date')
    associated_with_employee = models.ForeignKey(Employee)
    leave_count = models.DecimalField ('Count',default=0.0,max_digits=5,decimal_places=2)
