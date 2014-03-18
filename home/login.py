from django.db import IntegrityError

from django.shortcuts import render, redirect

from django.contrib.auth import login, logout, authenticate

from django.contrib.auth.models import User

def do_logout(request):
   logout(request)

   return redirect("/")

def login_view(request):
   return render(request, "home/login_register.html", request.GET)

def do_login(request):
   if request.POST:
      
      user = authenticate(
         username = request.POST.get('studentId'),
         password = request.POST.get('password'))

      if user is not None and user.is_active:
         login(request, user)

         redirect_path = request.POST.get("next", "/")
         if redirect_path == "":
            redirect_path = "/"

         return redirect(redirect_path)
      
   resp = redirect("login")
   parm = request.GET.copy()
   parm["invalid"] = "1"
   resp["Location"] += "?" + parm.urlencode()

   return resp


def do_register(request):
   if request.POST:

      username  = request.POST.get("studentId")

      firstname = request.POST.get("firstName")
      lastname  = request.POST.get("lastName")

      email     = request.POST.get("email")
      if email != request.POST.get("emailConfirm"):
         return redirect("/?emails_dont_match")

      password  = request.POST.get("password")
      if password != request.POST.get("passwordConfirm"):
         return redirect("/?passwords_dont_match")

      try:
         user = User.objects.create_user(
               request.POST.get("studentId"),
               request.POST.get("email"),
               request.POST.get("password"))
      except IntegrityError:
         return redirect("/?id_already_used")
         
      user.first_name = firstname
      user.last_name  = lastname
      user.save()

      user = authenticate(
            username=request.POST.get("studentId"),
            password=request.POST.get("password"))

      login(request, user)

   return redirect("/")





