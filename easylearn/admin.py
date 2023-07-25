# admin.py
from django.contrib import admin
from .models import AdmissionForm, AdminHOD, Staffs, Courses, Subjects, Students, Attendance, AttendanceReport, NotificationStudent, NotificationStaffs

admin.site.register(AdmissionForm)
admin.site.register(Students)
admin.site.register(Attendance)
admin.site.register(AttendanceReport)
admin.site.register(AdminHOD)
admin.site.register(Staffs)
admin.site.register(Courses)
admin.site.register(Subjects)
admin.site.register(NotificationStudent)
admin.site.register(NotificationStaffs)