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
    empId = models.CharField(max_length=256)
    startDate = models.DateField('start Date')
    leave_type = models.CharField(max_length=2, choices=LEAVE_TYPES_CHOICES)