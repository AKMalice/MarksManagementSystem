from django.db import models

class UserList(models.Model):
    username = models.CharField(max_length=50, unique=True)
    user_type = models.CharField(max_length=50)

class PassToken(models.Model):
    username = models.CharField(max_length=50)
    user_type = models.CharField(max_length=50)
    token = models.CharField(max_length=50)
    
