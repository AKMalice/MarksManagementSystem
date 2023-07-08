from django.contrib import admin
from analytics.models import *

class DisplayExams(admin.ModelAdmin):
    list_display = ('admin_username','name','course_id','max_marks','pass_marks','date')
    search_fields = ('admin_username',)

class DisplayResults(admin.ModelAdmin):
    list_display = ('admin_username','exam_id','student_id','marks')
    search_fields = ('admin_username',)

class DisplayUploads(admin.ModelAdmin):
    list_display = ('admin_username','teacher_id','exam_id','course_id','course_name','exam_name','section_name','file_name','date')
    search_fields = ('admin_username',)

admin.site.register(Exam,DisplayExams)
admin.site.register(Result,DisplayResults)
admin.site.register(Upload,DisplayUploads)