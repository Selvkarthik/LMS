from django.contrib import admin
from .models import Course, CourseVideo

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by')
    filter_horizontal = ('assigned_students',)

admin.site.register(CourseVideo)