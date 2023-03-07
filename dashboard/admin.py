from django.contrib import admin
from dashboard.models import Admin


class DisplayAdmins(admin.ModelAdmin):
    list_display = ('uni_name', 'username','email','password')
    search_fields = ('uni_name',)

admin.site.register(Admin,DisplayAdmins)
