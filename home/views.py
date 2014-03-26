from django.shortcuts import render
from django.http import HttpResponse

from home.models import Course

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

def course_selection(request):

    soencourses = Course.objects.filter(
        course_code__startswith="COEN"
    ).exclude(
        course_name__exact="None",
        description__exact="None"
    )
        

    context = {
        "courses"   : list(soencourses[:5]),
        "logged_in" : True
    }

    return render(request, 'home/course-selection.html', context)

def course_details(request):

    soencourses = Course.objects.filter(
        course_code__startswith="COEN"
    ).exclude(
        course_name__exact="None",
        description__exact="None"
    )
        

    context = {
        "courses"   : list(soencourses[:5]),
        "logged_in" : True
    }
    return render(request, 'home/course-details.html', context)