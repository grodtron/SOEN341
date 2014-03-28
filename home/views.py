from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required

from home.models import Course, CourseRequisites, ScheduleItem, ScheduleItemTime, Term, StudentRecord

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
    allbldgcourses = Course.objects.filter(course_code__startswith='BLDG').exclude(
        course_name__exact="None",
        description__exact="None"
    ).order_by('course_code')

    allcivicourses = Course.objects.filter(course_code__startswith='CIVI').exclude(
        course_name__exact="None",
        description__exact="None"
    ).order_by('course_code')

    allcoencourses = Course.objects.filter(course_code__startswith='COEN').exclude(
        course_name__exact="None",
        description__exact="None"
    ).order_by('course_code')

    allcompcourses = Course.objects.filter(course_code__startswith='COMP').exclude(
        course_name__exact="None",
        description__exact="None"
    ).order_by('course_code')

    alleleccourses = Course.objects.filter(course_code__startswith='ELEC').exclude(
        course_name__exact="None",
        description__exact="None"
    ).order_by('course_code')

    allinducourses = Course.objects.filter(course_code__startswith='INDU').exclude(
        course_name__exact="None",
        description__exact="None"
    ).order_by('course_code')

    allmechcourses = Course.objects.filter(course_code__startswith='MECH').exclude(
        course_name__exact="None",
        description__exact="None"
    ).order_by('course_code')

    allsoencourses = Course.objects.filter(course_code__startswith='SOEN').exclude(
        course_name__exact="None",
        description__exact="None"
    ).order_by('course_code')

    context = {
        "bldgcourses"   : list(allbldgcourses),
        "civicourses"   : list(allcivicourses),
        "coencourses"   : list(allcoencourses),
        "compcourses"   : list(allcompcourses),
        "eleccourses"   : list(alleleccourses),
        "inducourses"   : list(allinducourses),
        "mechcourses"   : list(allmechcourses),
        "soencourses"   : list(allsoencourses)
    }

    return render(request, 'home/course-selection.html', context)

@login_required
def course_details(request, course_code):
	
    course = Course.objects.filter(
        course_code__exact=course_code
    )
    prerequisites = CourseRequisites.objects.filter(
        course__exact=course
    )
    scheduleItems = ScheduleItem.objects.filter(
        course__exact=course
    )
    scheduleItemsTimes = ScheduleItemTime.objects.filter(
        schedule_item__exact=scheduleItems
    )

    context = {
        "course"               : course[0],
        "prereqs"              : list(prerequisites),
        "scheduleItems"        : list(scheduleItems),
        "scheduleItemsTimes"   : list(scheduleItemsTimes)
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

