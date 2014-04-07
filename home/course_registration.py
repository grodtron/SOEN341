import json

from django.http import HttpResponse

from django.core.exceptions import ObjectDoesNotExist

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from home.models import ShoppingCart, Course, StudentSchedule, ScheduleItemGroup, ScheduleItemTime

def json_response(code, data):
   return HttpResponse(json.dumps(data, sort_keys=True), status=code, content_type="application/json")

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
            "start" : str(time.start.hour)+':'+str(time.start.minute).zfill(2),
            "end"   : str(time. end .hour)+':'+str(time. end .minute).zfill(2)
         })

   d["times"] = t

   return d

def get_course_dict_from_group(group):
   course_dict = {}

   course_dict["course_info"] = {
      "schedule_item_group_id" : group.row_id,
      "course_id" : group.course.course_id,
      "code"      : group.course.course_code,
      "name"      : group.course.course_name,
      "credits"   : float(group.course.course_credits)
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
   
   return course_dict



@login_required
def get_registered_courses(request):
   schedule = StudentSchedule.objects.filter(user__exact=request.user)

   groups   = schedule.values_list('schedule_item_group', flat=True)

   courses = []

   for group in groups:
      group = ScheduleItemGroup.objects.get(row_id=group)

      courses.append(get_course_dict_from_group(group))

   return json_response(200, courses)

@login_required
def get_course_section(request, section_id):
   try:
      group = ScheduleItemGroup.objects.get(row_id=section_id)
   except ObjectDoesNotExist:
      return json_response(404, {"error":"no such course"})

   return json_response(200, get_course_dict_from_group(group))


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

def get_current_registered_times(request):
   # Get all ScheduleItemGroups for which the user is currently registered
   curr_item_groups = StudentSchedule.objects.select_related(
            'schedule_item_group'
         ).filter(
            user__exact=request.user
         )

   # Get all ScheduleItems for those ScheduleItemGroups
   curr_items = [
         get_schedule_items_for_schedule_item_group(_.schedule_item_group)
         for _ in curr_item_groups
   ]

   # Flatten it into one list
   # e.g.: [(1,2,3),(4,5),(6,7,8)] => [1,2,3,4,5,6,7,8]
   curr_items = reduce(lambda a, b: a+b, curr_items, [])

   # Get all ScheduleItemTimes for those ScheduleItems
   curr_times = ScheduleItemTime.objects.filter(schedule_item__in=curr_items)

   # Create a dictionary of schedule items by day
   days = {}
   for time in curr_times:
      if time.day.day_name in days:
         days[time.day.day_name].append(time)
      else:
         days[time.day.day_name] = [time]
   
   return days

@login_required
def register_for_course(request):
   if request.POST:
      id = request.POST.get("id")
      try:
         requested_group = ScheduleItemGroup.objects.select_related(
               'lecture','tutorial','lab'
         ).get(row_id__exact=id)
      except ObjectDoesNotExist:
         return json_response(400, {"error":"course with id '"+str(id)+"' does not exist"})

      requested_items = get_schedule_items_for_schedule_item_group(requested_group)

      requested_times = ScheduleItemTime.objects.filter(schedule_item__in=requested_items)

      current_registered_times = get_current_registered_times(request)

      for time in requested_times:
         try:
            potential_conflicts = current_registered_times[time.day.day_name]
         except KeyError:
            continue

         for potential_conflict in potential_conflicts:
            if not ((
                  time.start > potential_conflict.end and
                  time.end   > potential_conflict.end
               ) or (
                  time.start < potential_conflict.start and
                  time.end   < potential_conflict.start
            )):
               # TODO - indicate the conflicting class
               return json_response(409, {"error" : "there is a conflict"})

      # Here we have checked for conflicts and there's none, so we'll move on

      StudentSchedule.objects.create(
            schedule_item_group=requested_group,
            user=request.user)
      
      return json_response(200, {"success":"Successfully registered"})

   else:
      return json_response(400, {"error" : "no data sent"})


@login_required
def remove(request):
   if request.POST:
      id = request.POST.get("id")
      try:
         requested_group = ScheduleItemGroup.objects.get(row_id__exact=id)
      except ObjectDoesNotExist:
         return json_response(400, {"error":"course with id '"+str(id)+"' does not exist"})

      try:
         StudentSchedule.objects.get(
               schedule_item_group__exact=requested_group,
               user__exact=request.user
         ).delete()
      except ObjectDoesNotExist:
         return json_response(400, {"error":"you were not registered for course with id'" + str(id) + "'"})
      
      return json_response(200, {"success":"Successfully removed"})

   else:
      return json_response(400, {"error" : "no data sent"})


@login_required
def main(request):
   return render(request, 'registration/main.html', {})








