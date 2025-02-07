from django.contrib import admin
from . models import Teacher,Student,Course,Attendance,Marks,Subject
# Register your models here.
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Attendance)
admin.site.register(Marks)
admin.site.register(Subject)

