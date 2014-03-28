from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User

class Program(models.Model):
    program_id      = models.IntegerField(primary_key=True)
    program_name    = models.CharField(max_length=32)
    program_credits = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'programs'

class Course(models.Model):
    course_id      = models.IntegerField(primary_key=True)
    course_code    = models.CharField(max_length=16, blank=True)
    course_name    = models.CharField(max_length=255, blank=True)
    course_credits = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    description    = models.CharField(max_length=1200, blank=True)
    program        = models.ForeignKey(Program)
    class Meta:
        managed = False
        db_table = 'courses'

class ShoppingCart(models.Model):
   courses     = models.ManyToManyField(Course)
   user        = models.OneToOneField(User)

class CourseRequisites(models.Model):
    row_id              = models.IntegerField(primary_key=True)
    course              = models.ForeignKey(Course, related_name='+')
    requisite_course    = models.ForeignKey(Course, related_name='+')
    prerequisite        = models.BooleanField()
    class Meta:
        managed = False
        db_table = 'course_requisites'

class Term(models.Model):
    term_id = models.IntegerField(primary_key=True)
    term_name = models.CharField(max_length=16)
    class Meta:
        managed = False
        db_table = 'terms'


class CourseSequence(models.Model):
    row_id     = models.IntegerField(primary_key=True)
    program    = models.ForeignKey(Program)
    co_op      = models.BooleanField(db_column='co-op') # Field renamed to remove unsuitable characters.
    term       = models.ForeignKey(Term)
    year       = models.IntegerField()
    course     = models.ForeignKey(Course)
    core       = models.BooleanField()
    class Meta:
        managed = False
        db_table = 'course_sequences'

class CourseTerm(models.Model):
    row_id         = models.IntegerField(primary_key=True)
    course         = models.ForeignKey(Course)
    course_term    = models.ForeignKey(Term)
    year           = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'course_terms'

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


class Instructor(models.Model):
    instructor_id     = models.IntegerField(primary_key=True)
    instructor_fname  = models.CharField(max_length=32)
    instructor_lname  = models.CharField(max_length=32)
    instructor_email  = models.CharField(max_length=32)
    instructor_rating = models.DecimalField(max_digits=10, decimal_places=0)
    class Meta:
        managed = False
        db_table = 'instructors'


class Location(models.Model):
    location_id = models.IntegerField(primary_key=True)
    campus      = models.CharField(max_length=3)
    room_number = models.CharField(max_length=16)
    class Meta:
        managed = False
        db_table = 'locations'


class ScheduleItemType(models.Model):
    item_type_id   = models.IntegerField(primary_key=True)
    item_type_name = models.CharField(max_length=7)
    class Meta:
        managed = False
        db_table = 'schedule_item_types'


class ScheduleItem(models.Model):
    schedule_item_id = models.IntegerField(primary_key=True)
    course           = models.ForeignKey(Course)
    section          = models.CharField(max_length=2)
    item_type        = models.ForeignKey(ScheduleItemType)
    instructor       = models.ForeignKey(Instructor)
    location         = models.ForeignKey(Location)
    class Meta:
        managed = False
        db_table = 'schedule_items'


class ScheduleItemGroup(models.Model):
    row_id      = models.IntegerField(primary_key=True)
    course      = models.ForeignKey(Course)
    term        = models.ForeignKey(Term)
    lecture     = models.ForeignKey(ScheduleItem, blank=True, null=True, related_name='+')
    tutorial    = models.ForeignKey(ScheduleItem, blank=True, null=True, related_name='+')
    lab         = models.ForeignKey(ScheduleItem, blank=True, null=True, related_name='+')
    class Meta:
        managed = False
        db_table = 'schedule_item_groups'


class ScheduleItemTime(models.Model):
    row_id           = models.IntegerField(primary_key=True)
    schedule_item = models.ForeignKey(ScheduleItem)
    day           = models.ForeignKey(Day)
    start            = models.TimeField()
    end              = models.TimeField()
    class Meta:
        managed = False
        db_table = 'schedule_item_times'

class StudentRecord(models.Model):
    row_id  = models.IntegerField(primary_key=True)
    user    = models.ForeignKey(User)
    term    = models.ForeignKey(Term)
    year    = models.IntegerField()
    # TODO - probably should be changed to ForeignKey(Course)
    course_number = models.CharField(max_length=7)
    grade = models.CharField(max_length=3)
    class Meta:
        managed = False
        db_table = 'student_records'


class StudentSchedule(models.Model):
    row_id           = models.IntegerField(primary_key=True)
    user             = models.ForeignKey(User)
    schedule_item    = models.ForeignKey(ScheduleItem)
    class Meta:
        managed = False
        db_table = 'student_schedules'

