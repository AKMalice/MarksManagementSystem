from django.db import models

class Admin (models.Model):
    uni_name = models.fields.CharField(max_length=100,unique = True)
    username = models.fields.CharField(max_length=50,unique = True)
    email = models.fields.EmailField(max_length=100)
    password = models.fields.CharField(max_length=30)
