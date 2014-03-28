from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required

from home.models import Course, Term, StudentRecord

from login import login_view
from datetime import date

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

    soencourses = Course.objects.exclude(
        course_name__exact="None",
        description__exact="None"
    ).order_by('course_code')

    context = {
        "courses"   : list(soencourses),
    }

    return render(request, 'home/course-selection.html', context)

@login_required
def course_details(request, course_code):
	
    course = Course.objects.filter(
        course_code__exact=course_code
    )

    context = {
        "course"  : course[0]
    }
    return render(request, 'home/course-details.html', context)
        
@login_required
def edit_student_record(request):

  allterms = Term.objects.all()
  allyears = range(1990, date.today().year+1)
  allstudentrecords = StudentRecord.objects.filter(
    user_id__exact = request.user.id
  )
  allcourses = Course.objects.all()
  
  context = {
    "terms" : list(allterms),
    "years" : allyears[::-1],
    "studentrecords" : allstudentrecords,
    "courses" : list(allcourses)
  }
  return render(request , 'home/student-record-edit.html' , context)

#@login_required
#def save_student_record(request):
#  if request.POST:

