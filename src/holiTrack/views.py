#from django.template import Context, loader
from django.shortcuts import render_to_response
from holiTrack.models import Employee
#from django.http import HttpResponse
from django.http import Http404


def home(request):
    list_of_employees = Employee.objects.all()
    #output = ', ' .join([e.name for e in list_of_employees])
    #t = loader.get_template('templates/homepage.html')
    #c = Context({'list_of_employees': list_of_employees})
    #return HttpResponse(t.render(c))
    return render_to_response('templates/homepage.html',{'list_of_employees': list_of_employees})

def details(request, emp_id):
    try:
        e = Employee.objects.get(empId=emp_id);
    except Employee.DoesNotExist:
        raise Http404
    return render_to_response('templates/details.html',{'employee':e})
    