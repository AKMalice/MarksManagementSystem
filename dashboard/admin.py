from django.contrib import admin
from dashboard.models import Admin
from dashboard.models import Announcement
from dashboard.models import Faculty


class DisplayAdmins(admin.ModelAdmin):
    list_display = ('uni_name', 'username','email','password')
    search_fields = ('uni_name',)

class DisplayAnnouncements(admin.ModelAdmin):
    list_display = ('admin_username','note','time')
    search_fields = ('admin_username',)

class DisplayFaculty(admin.ModelAdmin):
    list_display = ('admin_username','teacher_id','name','email','username','password')
    search_fields = ('admin_username',)

admin.site.register(Admin,DisplayAdmins)
admin.site.register(Announcement,DisplayAnnouncements)
admin.site.register(Faculty,DisplayFaculty)
