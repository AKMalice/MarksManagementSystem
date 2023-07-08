from django.db import models

class Exam(models.Model):
    admin_username = models.fields.CharField(max_length=50)
    name = models.CharField(max_length=100)
    course_id = models.fields.CharField(max_length=50)
    max_marks = models.IntegerField()
    pass_marks = models.IntegerField()
    date =  models.DateField()

class Result(models.Model):
    admin_username = models.fields.CharField(max_length=50)
    exam_id = models.IntegerField()
    student_id = models.fields.CharField(max_length=50)
    marks = models.IntegerField()

class Upload(models.Model):
    admin_username = models.fields.CharField(max_length=50)
    teacher_id = models.fields.CharField(max_length=50)
    exam_id = models.IntegerField()
    course_name = models.CharField(max_length=100)
    course_id = models.fields.CharField(max_length=50)
    exam_name = models.CharField(max_length=100)
    section_name  = models.CharField(max_length=25)
    file_name = models.CharField(max_length=100)
    date = models.DateField()

    
    
