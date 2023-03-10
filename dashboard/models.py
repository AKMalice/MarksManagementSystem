from django.db import models

class Admin (models.Model):
    uni_name = models.fields.CharField(max_length=100,unique = True)
    username = models.fields.CharField(max_length=50,unique = True)
    email = models.fields.EmailField(max_length=100,unique = True)
    password = models.fields.CharField(max_length=30)

class Announcement (models.Model):
    admin_username = models.fields.CharField(max_length=50)
    note = models.fields.TextField(max_length=1000)
    time = models.DateTimeField(auto_now_add=True)

class Faculty(models.Model):
    admin_username = models.fields.CharField(max_length=50)
    teacher_id = models.fields.CharField(max_length=50,unique = True)
    name = models.fields.CharField(max_length=100)
    email = models.fields.EmailField(max_length=100,unique = True)
    username = models.fields.CharField(max_length=50,unique = True)
    password = models.fields.CharField(max_length=30)
