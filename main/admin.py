from django.contrib import admin

from .models import EduCenter, Course, Events, EducationType, Category, Level, Branch, Day


@admin.register(EduCenter)
class EduCenterAdmin(admin.ModelAdmin):
    list_display = [field.name for field in EduCenter._meta.fields]  
    search_fields = ['name', 'location'] 
    list_filter = ['edu_type', 'verify', 'partner']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Course._meta.fields] 
    search_fields = ['name', 'teacher']  
    list_filter = ['edu_center', 'level', 'intensive']


@admin.register(Events)
class EventsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Events._meta.fields]
    search_fields = ['name', 'location']  
    list_filter = ['edu_center', 'day']


admin.site.register(Category)
admin.site.register(EducationType)
admin.site.register(Level)
admin.site.register(Branch)
admin.site.register(Day)