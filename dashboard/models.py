from django.db import models

class Admin (models.Model):
    uni_name = models.fields.CharField(max_length=100,unique = True)
    username = models.fields.CharField(max_length=50,unique = True)
    email = models.fields.EmailField(max_length=100,unique = True)
    password = models.fields.CharField(max_length=30)

class Faculty(models.Model):
    admin_username = models.fields.CharField(max_length=50)
    teacher_id = models.fields.CharField(max_length=50)
    name = models.fields.CharField(max_length=100)
    email = models.fields.EmailField(max_length=100,unique = True)
    username = models.fields.CharField(max_length=50,unique = True)
    password = models.fields.CharField(max_length=30)

class Student(models.Model):
    admin_username = models.fields.CharField(max_length=50)
    student_id = models.fields.CharField(max_length=50)
    name = models.fields.CharField(max_length=100)
    email = models.fields.EmailField(max_length=100,unique = True)
    username = models.fields.CharField(max_length=50,unique = True)
    password = models.fields.CharField(max_length=30)

class Course(models.Model):
    admin_username = models.fields.CharField(max_length=50)
    course_id = models.fields.CharField(max_length=50)
    course_name = models.fields.CharField(max_length=100)

class Section(models.Model):
    admin_username = models.fields.CharField(max_length=50)
    teacher_id = models.fields.CharField(max_length=50)
    teacher_name = models.fields.CharField(max_length=100)
    course_id = models.fields.CharField(max_length=50)
    course_name = models.fields.CharField(max_length=100)
    section_id = models.fields.CharField(max_length=75)
    section_name = models.fields.CharField(max_length=25)
    year = models.fields.CharField(max_length=4)
    active = models.fields.BooleanField(default=True)


class Classe(models.Model):
    admin_username = models.fields.CharField(max_length=50)
    section_id = models.fields.CharField(max_length=75)
    student_id = models.fields.CharField(max_length=50)
    year = models.fields.CharField(max_length=4)

class Announcement (models.Model):
    admin_username = models.fields.CharField(max_length=50)
    note = models.fields.TextField(max_length=1000)
    time = models.DateTimeField(auto_now_add=True)
