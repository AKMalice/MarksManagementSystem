from django.contrib import admin
from django.contrib.auth.models import User
from home.models import UserList

class DisplayUsers(admin.ModelAdmin):
    list_display = ('username', 'user_type')
    search_fields = ('username',)

admin.site.register(UserList, DisplayUsers)
