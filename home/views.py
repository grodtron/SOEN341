from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required

from home.models import Course

from login import login_view

def index(request):
   if request.user.is_authenticated():
      return render(request, 'home/base.html', {})
   else:
      return login_view(request)


@login_required
def student_record(request):
    return render(request, 'home/student-record.html', {})

@login_required
def course_selection(request):

    soencourses = Course.objects.filter(
        course_code__startswith="COEN"
    ).exclude(
        course_name__exact="None",
        description__exact="None"
    )
        

    context = {
        "courses"   : list(soencourses[:5]),
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
