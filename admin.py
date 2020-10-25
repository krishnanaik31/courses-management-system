from django.contrib import admin
from django.db import models
from .models import Topic, Course, Student, Order
import decimal


def add_50_to_hours(ModelAdmin, request, queryset):
    for obj in queryset:
        obj.hours = obj.hours + decimal.Decimal('10.0')
        obj.save()


add_50_to_hours.short_description = "Add 10 hours to selected Courses"


class CourseAdmin(admin.ModelAdmin):
    list_display = ["name", "topic", "price", "hours", "for_everyone"]
    actions = [add_50_to_hours]

    class Meta:
        model = Course


class StudentAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "city"]

    def upper_case_name(self, obj):
        return ("%s %s" % (obj.first_name, obj.last_name)).upper()

    upper_case_name.short_description = "Student Full Name"


admin.site.register(Course, CourseAdmin)
admin.site.register(Topic)
admin.site.register(Student, StudentAdmin)
admin.site.register(Order)
