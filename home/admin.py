from django.contrib import admin
from django.contrib.auth.models import User
from home.models import *

class DisplayUsers(admin.ModelAdmin):
    list_display = ('username', 'user_type')
    search_fields = ('username',)

class DisplayPassTokens(admin.ModelAdmin):
    list_display = ('username','user_type','token')
    search_fields = ('username',)

admin.site.register(UserList, DisplayUsers)
admin.site.register(PassToken,DisplayPassTokens)
