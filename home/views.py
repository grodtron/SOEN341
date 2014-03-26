from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required

from home.models import Course, Term

from login import login_view

def index(request):
   if request.user.is_authenticated():
      return render(request, 'home/base.html', {})
   else:
      return login_view(request)


@login_required
def student_record(request):

  allterms = Term.objects.all()
  allyears = range(2010,2015)
  context = {
    "terms" : list(allterms),
    "years" : list(allyears)
  }
  return render(request, 'home/student-record.html', context)

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

@login_required
def edit_student_record(request):
  allterms = Term.objects.all()
  allyears = range(2010,2015)
  context = {
    "terms" : list(allterms),
    "years" : list(allyears)
  }
  return render(request , 'home/student-record-edit.html' , context)

