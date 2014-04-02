import json

from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from home.models import ShoppingCart, Course, ScheduleItemGroup

@login_required
def shopping_cart(request):
   cart, created = ShoppingCart.objects.get_or_create(user=request.user)

   courses = cart.courses.all().order_by('course_id')

   groups = ScheduleItemGroup.objects.select_related(
         'lecture','lab','tutorial'
   ).filter(course__in=courses, ).order_by('course')

   group_iter = iter(groups) 

   course_list = []
   g = next(group_iter)

   for course in courses:
      d = {"course":course}
      l = []
      try:
         while g.course == course:
            l.append(g)
            g = next(group_iter)
      except StopIteration:
         pass
      d["sections"] = l
      course_list.append(d)

   context = {"courses":course_list}

   return render(request, "shopping-cart/view.html", context)

@login_required
def remove(request):
   if request.POST:
      cart, created = ShoppingCart.objects.get_or_create(user=request.user)

      if not created:
         course = Course.objects.get(course_id=request.POST.get("course"))

         cart.courses.remove(course)

   return get_cart_dict(cart)


def get_cart_dict(cart):
   courses = cart.courses.values('course_id', 'course_code', 'course_name')

   return HttpResponse(json.dumps(list(courses)), content_type="applicationn/json")


@login_required
def add(request):
   if request.POST:
      cart, created = ShoppingCart.objects.get_or_create(user=request.user)

      course = Course.objects.get(course_id=request.POST.get("course"))

      cart.courses.add(course)
      cart.save()

   return get_cart_dict(cart)


@login_required
def get_cart(request):
    if request.user.is_authenticated():
       cart, created = ShoppingCart.objects.get_or_create(user=request.user)

    return get_cart_dict(cart)
   
