from django.template import Context, loader
from django.shortcuts import render_to_response
from holiTrack.models import Employee
from django.http import HttpResponse

def home(request):
    list_of_employees = Employee.objects.all()
    #output = ', ' .join([e.name for e in list_of_employees])
    #t = loader.get_template('templates/homepage.html')
    #c = Context({'list_of_employees': list_of_employees})
    #return HttpResponse(t.render(c))
    return render_to_response('templates/homepage.html',{'list_of_employees': list_of_employees})