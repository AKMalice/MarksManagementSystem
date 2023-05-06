from django.contrib import admin
from dashboard.models import Admin,Announcement,Faculty,Course,Section,Student,Classe


class DisplayAdmins(admin.ModelAdmin):
    list_display = ('uni_name', 'username','email','password')
    search_fields = ('uni_name',)

class DisplayAnnouncements(admin.ModelAdmin):
    list_display = ('admin_username','note','time')
    search_fields = ('admin_username',)

class DisplayFaculty(admin.ModelAdmin):
    list_display = ('admin_username','teacher_id','name','email','username','password')
    search_fields = ('admin_username',)

class DisplayStudent(admin.ModelAdmin):
    list_display = ('admin_username','student_id','name','email','username','password')
    search_fields = ('admin_username',)

class DisplayCourse(admin.ModelAdmin):
    list_display = ('admin_username','course_id','course_name')
    search_fields = ('admin_username',)

class DisplaySection(admin.ModelAdmin):
    list_display = ('admin_username','teacher_id','teacher_name','course_id','course_name','section_id','section_name','year','active')
    search_fields = ('admin_username',)

class DisplayClasses(admin.ModelAdmin):
    list_display = ('admin_username','section_id','student_id','year')

admin.site.register(Admin,DisplayAdmins)
admin.site.register(Announcement,DisplayAnnouncements)
admin.site.register(Faculty,DisplayFaculty)
admin.site.register(Course,DisplayCourse)
admin.site.register(Section,DisplaySection)
admin.site.register(Student,DisplayStudent)
admin.site.register(Classe,DisplayClasses)
