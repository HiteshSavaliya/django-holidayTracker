from django.db import models
from django.utils import timezone
from datetime import datetime

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
    calenderYear = models.DateField('Calender Year',default=datetime.now())
    startDate = models.DateField('start Date',default=datetime.now())
    remainingLeave = models.DecimalField('Remaining leave',max_digits=5,decimal_places=2)
    leave = models.DecimalField ('Applied leave',max_digits=5,decimal_places=2)
    total = models.DecimalField(max_digits=5,decimal_places=2)
    leave_type = models.CharField(max_length=2, choices=LEAVE_TYPES_CHOICES)
    
    def __init__(self,*args,**kwargs):
        print "__init__"
        models.Model.__init__(self,*args,**kwargs)
        self.calenderYear = timezone.now()