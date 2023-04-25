from django.contrib import admin

# 从models导入这些class，这样下面的admin.site.register语句才能认识这些class
from .models import Semester, Section, Course, Instructor, Student, Registration, Period, Year

admin.site.register(Period)
admin.site.register(Year)
admin.site.register(Semester)
admin.site.register(Section)
admin.site.register(Course)
admin.site.register(Instructor)
admin.site.register(Student)
admin.site.register(Registration)