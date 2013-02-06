'''
Created on Feb 5, 2013

@author: hiteshsavaliya
'''

import os
from icalendar import Calendar
import datetime
from datetime import date

#from django.utils.datetime_safe import datetime

class icsParser:
    publicholidays = set()
    
    def parse(self):
        print 'ICS Parse'
        directory = os.path.dirname(__file__)
        icsFileName = os.path.join(directory,'england-and-wales.ics')

#       Read ics file and create 
        calData = Calendar.from_ical (open(icsFileName,'r').read())
        events = calData.walk('VEVENT')

        for publicHoliday in events:
            holidayStartDate = publicHoliday.decoded('DTSTART')
            holidayEndDate = publicHoliday.decoded('DTEND')
#            print holidayStartDate
#            print holidayEndDate
            
            currentYear = datetime.date.today().year
            
            if holidayStartDate.year == currentYear:
                self.publicholidays.add(holidayStartDate)
                
            if holidayEndDate == currentYear:
                self.publicholidays.add(holidayEndDate)

        print self.publicholidays

    def is_holiday(self,in_date):
        if in_date is not None:
            return in_date in self.publicholidays
        return False 