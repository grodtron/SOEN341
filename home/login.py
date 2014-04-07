from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from django.shortcuts import render, redirect

from django.contrib.auth import login, logout, authenticate

from django.contrib.auth.models import User
from home.models import ForgotPasswordCode

from django.conf import settings

from os import urandom
from binascii import b2a_base64

from smtplib import SMTP

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

def get_random_code():
   code = "="
   while '=' in code or '+' in code or '/' in code:
      code = b2a_base64(urandom(6))[:8]
   return code


def do_forgot_password(request):
   if request.POST:
      email = request.POST.get("email")
      try:
         user = User.objects.get(email=email)
      except ObjectDoesNotExist:
         return redirect("/")

      try:
         code_obj = ForgotPasswordCode.objects.get(user=user)
         code = code_obj.code
      except ObjectDoesNotExist:
         while True:
            try:
               code = get_random_code()
               ForgotPasswordCode.objects.create(user=user, code=code) 
               break
            except IntegrityError:
               continue
                 

      smtp = SMTP()
      smtp.connect(settings.FORGOT_PW_EMAIL_SERVER)
      smtp.login(settings.FORGOT_PW_EMAIL_USER, settings.FORGOT_PW_EMAIL_PASS)

      smtp.sendmail(settings.FORGOT_PW_EMAIL_FROMADDR, user.email, 
         "From: "+settings.FORGOT_PW_EMAIL_FROMADDR+"\r\n"         
        +"To: "+user.email+"\r\n"
        +"Subject: WizReg password reset\r\n"
      +"""
      Please reset your password at the following link:

      http://wizreg.char1es.webfactional.com/reset-password/%s
      """ % code,
      )
   return redirect('/')

def reset_password(request, code):
   try:
      code_obj = ForgotPasswordCode.objects.get(code=code)
   except ObjectDoesNotExist:
      return redirect('/')

   return render(request, 'home/reset-password.html', {"code":code})

def do_reset_password(request):
   
   if request.POST:

      code = request.POST.get("code")

      password = request.POST.get("password")
      if password != request.POST.get("passwordConfirm"):
         return redirect("/reset-password/" + code + "?passwords_dont_match")

      try:
         code_obj = ForgotPasswordCode.objects.select_related('user').get(code=code)
         user = code_obj.user 
      except ObjectDoesNotExist:
         return redirect('/')

      code_obj.delete()

      user.set_password(password)
      user.save()
         

   return redirect("/")
