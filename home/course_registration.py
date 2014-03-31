import json

from django.http import HttpResponse

from django.core.exceptions import ObjectDoesNotExist

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from home.models import ShoppingCart, Course, StudentSchedule, ScheduleItemGroup, ScheduleItemTime

def fill_schedule_item_dict(item):

   """This function creates a dictionary for the given ScheduleItem
      (intended for use when serializing to JSON
   """
   d = {}

   d["id"]         = item.schedule_item_id
   d["section"]    = item.section
   t = []

   times = ScheduleItemTime.objects.filter(schedule_item__exact=item)
   for time in times:
      t.append({
            "day"   : time.day.day_name,
            "start" : str(time.start),
            "end"   : str(time.end)
         })

   d["times"] = t

   return d

@login_required
def get_registered_courses(request):
   schedule = StudentSchedule.objects.filter(user__exact=request.user)

   groups   = schedule.values_list('schedule_item_group', flat=True)

   courses = []

   for group in groups:
      group = ScheduleItemGroup.objects.get(row_id=group)

      course_dict = {}

      course_dict["course_info"] = {
         "id"      : group.course.course_id,
         "code"    : group.course.course_code,
         "name"    : group.course.course_name,
         "credits" : float(group.course.course_credits)
      }

      try:
         lecture = group.lecture
      except ObjectDoesNotExist:
         lecture = False

      if lecture:
         course_dict["lec"] = fill_schedule_item_dict(lecture)
      
      try:
         tut = group.tutorial
      except ObjectDoesNotExist:
         tut = False

      if tut:
         course_dict["tut"] = fill_schedule_item_dict(tut)

      try:
         lab = group.lab
      except ObjectDoesNotExist:
         lab = False

      if lab:
         course_dict["lab"] = fill_schedule_item_dict(lab)

      courses.append(course_dict)

   return HttpResponse(json.dumps(list(courses)), content_type="applicationn/json")


def get_schedule_items_for_schedule_item_group(group):
   l = []
   try:
      l.append(group.lecture)
   except ObjectDoesNotExist:
      pass
   try:
      l.append(group.tutorial)
   except ObjectDoesNotExist:
      pass
   try:
      l.append(group.lab)
   except ObjectDoesNotExist:
      pass
   return l

@login_required
def register_for_course(request):
   #if request.POST:
      id = request.POST.get("id")
      try:
         sched_group = ScheduleItemGroup.objects.get(row_id__exact=id)
      except ObjectDoesNotExist:
         data = {"error":"course with id '"+str(id)+"' does not exist"}

      curr_item_groups = StudentSchedule.objects.select_related(
               'schedule_item_group'
            ).filter(
               user__exact=request.user
            )

      # such bad hackery. wow.
      curr_items = [
            get_schedule_items_for_schedule_item_group(_.schedule_item_group)
            for _ in curr_item_groups
      ]

      curr_items = reduce(lambda a, b: a+b, curr_items)

      curr_items = [item.schedule_item_id for item in curr_items]

      curr_times = ScheduleItemTime.objects.select_related().filter(schedule_item__in=curr_items)

      days = {}

      for time in curr_times:
         if time.day.day_name in days:
            days[time.day.day_name].append(time)
         else:
            days[time.day.day_name] = [time]
      
      return HttpResponse(json.dumps(curr_item_groups), content_type="applicationn/json")
       

       
   #else:
   #   data = {"error":"no data sent"}











