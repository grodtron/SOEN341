from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from home.models import ShoppingCart, Course

@login_required
def shopping_cart(request):
   cart, created = ShoppingCart.objects.get_or_create(user=request.user)

   courses = cart.courses.all()

   context = {"courses":courses}

   return render(request, "shopping-cart/view.html", context)

@login_required
def remove(request):
   if request.POST:
      cart, created = ShoppingCart.objects.get_or_create(user=request.user)

      if not created:
         course = Course.objects.get(course_id=request.POST.get("course"))

         cart.courses.remove(course)


   return redirect("/shopping-cart")

@login_required
def add(request):
   if request.POST:
      cart, created = ShoppingCart.objects.get_or_create(user=request.user)

      if not created:
         course = Course.objects.get(course_id=request.POST.get("course"))

         cart.courses.add(course)
         cart.save()


   return redirect("/shopping-cart")
   
