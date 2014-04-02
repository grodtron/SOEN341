from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required

from home.models import Course, CourseRequisites, ScheduleItem, ScheduleItemTime, Term, StudentRecord, ShoppingCart, ScheduleItemGroup, Location

from login import login_view
from datetime import date

def index(request):
   if request.user.is_authenticated():
      return render(request, 'home/base.html', {})
   else:
      return login_view(request)

@login_required
def schedule(request):
  return render(request , 'home/schedule.html', {})

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
def course_selection(request,program=None):
    shopping_cart, created = ShoppingCart.objects.get_or_create(user=request.user)
    shopping_cart = shopping_cart.courses.all()
    if program != None:
        programcourses = Course.objects.filter(course_code__startswith=program).exclude(
            course_name__exact="None",
            description__exact="None"
        ).order_by('course_code')
        context = {
            "courses"   : list(programcourses),
            "shoppingCart" : shopping_cart
        }
    else:
        context = {
            "courses"   : list(),
            "shoppingCart" : shopping_cart
        }
    return render(request, 'home/course-selection.html', context)

@login_required
def course_details(request, course_code):
	
    course = Course.objects.filter(
        course_code__exact=course_code
    )
    prerequisites = CourseRequisites.objects.filter(
        course__exact=course,
		prerequisite__exact=1
    )
    
    corequisites = CourseRequisites.objects.filter(
        course__exact=course,
        prerequisite__exact=0
    )
	
    scheduleItems = ScheduleItem.objects.filter(
        course__exact=course
    )
    scheduleItemsGroups = ScheduleItemGroup.objects.filter(
        course__exact= course
    )
    scheduleItemsTimes = ScheduleItemTime.objects.filter(
        schedule_item__exact=scheduleItems
    )
    
    locations = Location.objects.filter(
        
    )
    
    department_temp = course_code
    
    shopping_cart, created = ShoppingCart.objects.get_or_create(user=request.user)
    shopping_cart = shopping_cart.courses.all()
    
    context = {
        "course"               : course[0],
        "prereqs"              : list(prerequisites),
        "coreqs"               : list(corequisites),
        "scheduleItems"        : list(scheduleItems),
        "scheduleItemsTimes"   : list(scheduleItemsTimes),
        "department"           : department_temp,
        "shoppingCart"         : shopping_cart,
        "scheduleItemsGroups"  : list(scheduleItemsGroups),
        "locations"            : list(locations)
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

