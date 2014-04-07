from django.contrib.auth import login, logout, authenticate
from django.test import TestCase

from django.test.client import Client

from django.contrib.auth.models import User

from home.models import *

import json

class LoginTests(TestCase):

   def test_login_when_registered(self):
      username = "foobar"
      password = "password"
      user = User.objects.create_user(username, "foo@bar.com", password)

      client = Client()

      response = client.post("/do-login", {"studentId":username, "password":password})

      self.assertEquals(response.status_code, 302)
      self.assertEquals(response["Location"], "http://testserver/")

      self.assertEquals(user.is_authenticated(), True)

   def test_login_when_not_registered(self):

      client = Client()

      response = client.post("/do-login", {"studentId":"foobar", "password":"password"})

      self.assertEquals(response.status_code, 302)
      self.assertEquals(response["Location"], "http://testserver/login?invalid=1")

   def test_register_when_valid(self):

      client = Client()

      response = client.post("/do-register", { "studentId":"test",
               "firstName":"Testfirst", "lastName":"Testlast",
               "email":"foo@bar.com",   "emailConfirm":"foo@bar.com",
               "password":"pass",       "passwordConfirm":"pass"})

      self.assertEquals(response.status_code, 302)
      self.assertEquals(response["Location"], "http://testserver/")

      user = authenticate(username="test", password="pass")

      self.assertEquals(user.first_name, "Testfirst")
      self.assertEquals(user.last_name, "Testlast")
      self.assertEquals(user.email, "foo@bar.com")
               
   def test_register_when_passwords_dont_match(self):

      client = Client()

      response = client.post("/do-register", { "studentId":"test",
               "firstName":"Testfirst", "lastName":"Testlast",
               "email":"foo@bar.com",   "emailConfirm":"foo@bar.com",
               "password":"pass",       "passwordConfirm":"password"})

      self.assertEquals(response.status_code, 302)
      self.assertEquals(response["Location"], "http://testserver/?passwords_dont_match")

      self.assertIsNone(authenticate(username="test", password="pass"))

   def test_register_when_emails_dont_match(self):

      client = Client()

      response = client.post("/do-register", { "studentId":"test",
               "firstName":"Testfirst", "lastName":"Testlast",
               "email":"foo@bar.com",   "emailConfirm":"foo@bar.ca",
               "password":"pass",       "passwordConfirm":"pass"})

      self.assertEquals(response.status_code, 302)
      self.assertEquals(response["Location"], "http://testserver/?emails_dont_match")

      self.assertIsNone(authenticate(username="test", password="pass"))

   def test_register_when_id_already_exists(self):

      User.objects.create(username="test")

      client = Client()

      response = client.post("/do-register", { "studentId":"test",
               "firstName":"Testfirst", "lastName":"Testlast",
               "email":"foo@bar.com",   "emailConfirm":"foo@bar.com",
               "password":"pass",       "passwordConfirm":"pass"})

      self.assertEquals(response.status_code, 302)
      self.assertEquals(response["Location"], "http://testserver/?id_already_used")


class CourseRegistrationTests(TestCase):

   def test_get_course_section_when_exists(self):
      username = "foobar"
      password = "password"
      user = User.objects.create_user(username, "foo@bar.com", password)

      client = Client()

      client.login(username=username, password=password)

      response = client.get("/register/get-course/253000000")

      self.assertEquals(response.status_code, 404)

   def test_get_course_section_when_not_exists(self):
      username = "foobar"
      password = "password"
      user = User.objects.create_user(username, "foo@bar.com", password)

      client = Client()

      client.login(username=username, password=password)
      response = client.get("/register/get-course/253")

      self.assertEquals(response.status_code, 200)
      self.assertEquals(json.dumps(json.loads(response.content)), json.dumps(json.loads('{"course_info":'+
      '{"code": "BLDG212", "course_id": 107, "credits": 3.0, "name": "Building En'+
      'gineering Drawing and Introduction to Design", "schedule_item_group_id": 2'+
      '53}, "lec": {"id": 339, "section": "L", "times": [{"day": "Monday", "end":'+
      '"13:00", "start": "10:15"}]}, "tut": {"id": 341, "section": "LB", "times":'+
      '[{"day": "Monday", "end": "15:05", "start": "13:15"}]}}')))


   def test_remove_when_not_registered(self):
      username = "foobar"
      password = "password"
      user = User.objects.create_user(username, "foo@bar.com", password)

      client = Client()

      client.login(username=username, password=password)

      response = client.post("/register/do-remove", {"id":1427})
      self.assertEquals(response.status_code, 400)

   def test_remove_when_registered(self):
      username = "foobar"
      password = "password"
      user = User.objects.create_user(username, "foo@bar.com", password)

      StudentSchedule.objects.create(
            user=user,
            schedule_item_group_id=1427) # COEN346

      client = Client()

      client.login(username=username, password=password)

      response = client.post("/register/do-remove", {"id":1427})
      self.assertEquals(response.status_code, 200)

   def test_register_when_no_conflict(self):
      username = "foobar"
      password = "password"
      user = User.objects.create_user(username, "foo@bar.com", password)

      client = Client()

      client.login(username=username, password=password)

      response = client.post("/register/do-add", {"id":253})
      self.assertEquals(response.status_code, 200)

   def test_register_when_conflict(self):
      username = "foobar"
      password = "password"
      user = User.objects.create_user(username, "foo@bar.com", password)
      
      StudentSchedule.objects.create(
            user=user,
            schedule_item_group_id=1427) # COEN346
      StudentSchedule.objects.create(
            user=user,
            schedule_item_group_id=1469) # ELEC353
      StudentSchedule.objects.create(
            user=user,
            schedule_item_group_id=1458) # ELEC321
      StudentSchedule.objects.create(
            user=user,
            schedule_item_group_id=1384) # SOEN341

      client = Client()

      client.login(username=username, password=password)

      response = client.post("/register/do-add", {"id":253})
      self.assertEquals(response.status_code, 409)

   def test_get_registered_courses_when_registered(self):
      username = "foobar"
      password = "password"
      user = User.objects.create_user(username, "foo@bar.com", password)
      
      StudentSchedule.objects.create(
            user=user,
            schedule_item_group_id=1427) # COEN346
      StudentSchedule.objects.create(
            user=user,
            schedule_item_group_id=1469) # ELEC353
      StudentSchedule.objects.create(
            user=user,
            schedule_item_group_id=1458) # ELEC321
      StudentSchedule.objects.create(
            user=user,
            schedule_item_group_id=1384) # SOEN341

      client = Client()

      client.login(username=username, password=password)

      response = client.get("/register/get-courses")

      self.assertEquals(response.status_code, 200)
      self.assertEquals(json.dumps(json.loads(response.content)),
            json.dumps(json.loads('[{"course_info": {"code": "COEN346",'+
      '"course_id": 402, "credits": 4.0, "name": "Operating Systems", "schedule'+
      '_item_group_id": 1427}, "lab": {"id": 1949, "section": "YJ", "times": [{"'+
      'day": "Tuesday", "end": "20:15", "start": "17:45"}]}, "lec": {"id": 1946'+
      ', "section": "Y", "times": [{"day": "Tuesday", "end": "11:30", "start": '+
      '"8:45"}]}, "tut": {"id": 1947, "section": "YA", "times": [{"day": "Monda'+
      'y", "end": "13:05", "start": "12:15"}]}}, {"course_info": {"code": "ELEC'+
      '353", "course_id": 413, "credits": 3.0, "name": "Transmission Lines, Wav'+
      'es and Signal Integrity", "schedule_item_group_id": 1469}, "lec": {"id":'+
      '2010, "section": "W", "times": [{"day": "Wednesday", "end": "11:30", "sta'+
      'rt": "10:15"}, {"day": "Friday", "end": "11:30", "start": "10:15"}]}, "t'+
      'ut": {"id": 2011, "section": "WA", "times": [{"day": "Friday", "end": "1'+
      '4:05", "start": "13:15"}]}}, {"course_info": {"code": "ELEC321", "course'+
      '_id": 411, "credits": 3.5, "name": "Introduction to Semiconductor Materi'+
      'als and Devices", "schedule_item_group_id": 1458}, "lab": {"id": 1994, "'+
      'section": "HL", "times": [{"day": "Thursday", "end": "16:00", "start": "'+
      '13:15"}]}, "lec": {"id": 1989, "section": "H", "times": [{"day": "Tuesda'+
      'y", "end": "17:30", "start": "16:15"}, {"day": "Thursday", "end": "17:30'+
      '", "start": "16:15"}]}, "tut": {"id": 1990, "section": "HA", "times": [{'+
      '"day": "Tuesday", "end": "14:05", "start": "13:15"}]}}, {"course_info": '+
      '{"code": "SOEN341", "course_id": 195, "credits": 3.0, "name": "Software '+
      'Process", "schedule_item_group_id": 1384}, "lec": {"id": 1882, "section"'+
      ': "S", "times": [{"day": "Wednesday", "end": "10:00", "start": "8:45"}, '+
      '{"day": "Friday", "end": "10:00", "start": "8:45"}]}, "tut": {"id": 1885'+
      ', "section": "SC", "times": [{"day": "Friday", "end": "15:05", "start": '+
      '"14:15"}]}}]')))


   def test_get_registered_courses_when_not_registered(self):
      username = "foobar"
      password = "password"
      User.objects.create_user(username, "foo@bar.com", password)
      
      client = Client()

      client.login(username=username, password=password)

      response = client.get("/register/get-courses")

      self.assertEquals(response.status_code, 200)
      self.assertEquals(response.content, "[]")


