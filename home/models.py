# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order (TODO)
#   * Make sure each model has one field with primary_key=True (DONE)
#   * Remove `managed = False` lines for those models you wish to give write DB access (TODO)
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

# DONE
class CourseRequisites(models.Model):
    row_id              = models.IntegerField(primary_key=True)
    course_id           = models.ForeignKey(Course)
    requisite_course_id = models.ForeignKey(Course)
    prerequisite        = models.BooleanField()
    class Meta:
        managed = False
        db_table = 'course_requisites'

#DONE
class CourseSequences(models.Model):
    row_id     = models.IntegerField(primary_key=True)
    program_id = models.ForeignKey(Program)
    co_op      = models.BooleanField(db_column='co-op') # Field renamed to remove unsuitable characters.
    term_id    = models.ForeignKey(Term)
    year       = models.IntegerField()
    course_id  = models.ForeignKey(Course)
    core       = models.BooleanField()
    class Meta:
        managed = False
        db_table = 'course_sequences'

#DONE
class CourseTerms(models.Model):
    row_id         = models.IntegerField(primary_key=True)
    course_id      = models.ForeignKey(Course)
    course_term_id = models.ForeignKey(Term)
    year           = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'course_terms'

#DONE
class Course(models.Model):
    course_id      = models.IntegerField(primary_key=True)
    course_code    = models.CharField(max_length=16, blank=True)
    course_name    = models.CharField(max_length=255, blank=True)
    course_credits = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    description    = models.CharField(max_length=1200, blank=True)
    program_id     = models.ForeignKey(Program)
    class Meta:
        managed = False
        db_table = 'courses'

#DONE
class Day(models.Model):
    day_id = models.IntegerField(primary_key=True)
    day_name = models.CharField(max_length=16)
    class Meta:
        managed = False
        db_table = 'days'

# @Charles - can you please verify that this table's primary key is correct,
# I had to modify it
#   - Gordon
class Grade(models.Model):
    grade       = models.CharField(primary_key=True, max_length=3)
    point_value = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'grades'

#DONE
class Instructor(models.Model):
    instructor_id     = models.IntegerField(primary_key=True)
    instructor_fname  = models.CharField(max_length=32)
    instructor_lname  = models.CharField(max_length=32)
    instructor_email  = models.CharField(max_length=32)
    instructor_rating = models.DecimalField(max_digits=10, decimal_places=0)
    class Meta:
        managed = False
        db_table = 'instructors'

#DONE
class Location(models.Model):
    location_id = models.IntegerField(primary_key=True)
    campus      = models.CharField(max_length=3)
    room_number = models.CharField(max_length=16)
    class Meta:
        managed = False
        db_table = 'locations'

#DONE
class Program(models.Model):
    program_id      = models.IntegerField(primary_key=True)
    program_name    = models.CharField(max_length=32)
    program_credits = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'programs'

#DONE
class ScheduleItemGroup(models.Model):
    row_id      = models.IntegerField(primary_key=True)
    course_id   = models.ForeignKey(Course)
    term_id     = models.ForeignKey(Term)
    lecture_id  = models.ForeignKey(ScheduleItem, blank=True, null=True)
    tutorial_id = models.ForeignKey(ScheduleItem, blank=True, null=True)
    lab_id      = models.ForeignKey(ScheduleItem, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'schedule_item_groups'

#DONE
class ScheduleItemTime(models.Model):
    row_id           = models.IntegerField(primary_key=True)
    schedule_item_id = models.ForeignKey(ScheduleItem)
    day_id           = models.ForeignKey(Day)
    start            = models.TimeField()
    end              = models.TimeField()
    class Meta:
        managed = False
        db_table = 'schedule_item_times'

#DONE
class ScheduleItemType(models.Model):
    item_type_id   = models.IntegerField(primary_key=True)
    item_type_name = models.CharField(max_length=7)
    class Meta:
        managed = False
        db_table = 'schedule_item_types'

#DONE
class ScheduleItem(models.Model):
    schedule_item_id = models.IntegerField(primary_key=True)
    course_id        = models.ForeignKey(Course)
    section          = models.CharField(max_length=2)
    item_type_id     = models.ForeignKey(ScheduleItemType)
    instructor_id    = models.FoireignKey(Instructor)
    location_id      = models.ForeignKey(Location)
    class Meta:
        managed = False
        db_table = 'schedule_items'

#DONE
class StudentRecord(models.Model):
    row_id  = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(User)
    term_id = models.ForeignKey(Term)
    year    = models.IntegerField()
    # TODO - probably should be changed to ForeignKey(Course)
    course_number = models.CharField(max_length=7)
    grade = models.CharField(max_length=3)
    class Meta:
        managed = False
        db_table = 'student_records'

#DONE
class StudentSchedule(models.Model):
    row_id           = models.IntegerField(primary_key=True)
    user_id          = models.ForeignKey(User)
    schedule_item_id = models.ForeignKey(ScheduleItem)
    class Meta:
        managed = False
        db_table = 'student_schedules'

#DONE
class Term(models.Model):
    term_id = models.IntegerField(primary_key=True)
    term_name = models.CharField(max_length=16)
    class Meta:
        managed = False
        db_table = 'terms'

#DONE
class UserLogin(models.Model):
    user_id = models.IntegerField(primary_key=True)
    password = models.CharField(max_length=32)
    class Meta:
        managed = False
        db_table = 'user_logins'

#DONE
class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    user_fname = models.CharField(max_length=32)
    user_lname = models.CharField(max_length=32)
    user_email = models.CharField(max_length=32)
    credits_earned = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'users'

