from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context = {
        "logged_in" : True
    }
    return render(request, 'home/base.html', context)

def student_record(request):
    context = {
        "logged_in" : True
    }
    return render(request, 'home/student-record.html', context)

