from django.db import models

LEAVE_TYPES_CHOICES = (
#        ('0', 'Working'),
        ('0', 'None'),
        ('1', 'Sick'),
        ('2', 'Vacation'),
#        ('3', 'Bank Holiday'),
        ('4', 'Business Trip'),
#        ('5','Weekend'),
        ('6','Other'),
    )

class Employee (models.Model):
    
    def __unicode__(self):
        return self.name;
    
    name = models.CharField(max_length=256)
    email = models.EmailField(max_length=254,null=True)
#    empId = models.AutoField(primary_key=True)
    calenderYear = models.DateField('Calender Year',blank=True,null=True)
    startDate = models.DateField('Join Date',blank=True,null=True)
    remainingLeave = models.DecimalField('Remaining leave',max_digits=5,decimal_places=2)
    leave = models.DecimalField ('Applied leave',default=0.0,max_digits=5,decimal_places=2)
    leaveFrom = models.DateField ('From',blank=True,null=True)
    leaveTo = models.DateField ('To',blank=True,null=True)
    total = models.DecimalField(max_digits=5,decimal_places=2)
    leave_type = models.CharField(max_length=2,default=0,choices=LEAVE_TYPES_CHOICES)
    
#    def __init__(self,*args,**kwargs):
#        print "Employee __init__"
#        models.Model.__init__(self,*args,**kwargs)
#        self.calenderYear = datetime.date(datetime.date.today().year,1,1)
#        self.startDate = self.calenderYear


class ApprovedLeaveHistory(models.Model):
    
    def __unicode__(self): 
#        return 'Leave : ' + LEAVE_TYPES_CHOICES[int(self.leave_type)][1]
#        return self.get_leave_type_display()
        return 'Leave instance: %d' %self.leaveId

    leaveId = models.IntegerField(default=0,blank=True,null=True)
    leave_start_date = models.DateField('Start Date',blank=True,null=True)
    leave_end_date = models.DateField('End Date',blank=True,null=True)
    associated_with_employee = models.ForeignKey(Employee)
    leave_count = models.DecimalField ('Leave Count',default=0.0,max_digits=5,decimal_places=2)
    leave_type = models.CharField('Leave Type',max_length=2,default=0,choices=LEAVE_TYPES_CHOICES)
