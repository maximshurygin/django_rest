from django.contrib import admin

from learning.models import Course, Lesson


# Register your models here.

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'image', 'description', 'owner']
    search_fields = ('title', 'description',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'image', 'video_url', 'course', 'owner']
    search_fields = ('title', 'description',)
