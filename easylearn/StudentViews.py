from django.shortcuts import render, redirect
import datetime
from django.contrib import messages
from .models import Students, Attendance, AttendanceReport, Courses, Subjects,StudentResult,CustomUser

def student_home(request):
    # Get the currently logged-in student
    student = Students.objects.get(user=request.user)

    # Get the Students's attendance data
    total_attendance = AttendanceReport.objects.filter(student=student).count()
    attendance_present = AttendanceReport.objects.filter(student=student, status=True).count()
    attendance_absent = AttendanceReport.objects.filter(student=student, status=False).count()

    # Get the total number of subjects for the student's course
    total_subjects = Subjects.objects.filter(course=student.course).count()

    # Get the names and attendance data for all subjects of the student's course
    subjects = Subjects.objects.filter(course=student.course)
    subject_data = []
    for subject in subjects:
        attendance = Attendance.objects.filter(subject=subject)
        attendance_present_count = AttendanceReport.objects.filter(attendance__in=attendance, status=True, student=student).count()
        attendance_absent_count = AttendanceReport.objects.filter(attendance__in=attendance, status=False, student=student).count()
        subject_data.append({
            'name': subject.name,
            'present': attendance_present_count,
            'absent': attendance_absent_count
        })

    context = {
        'student': student,
        'total_attendance': total_attendance,
        'attendance_present': attendance_present,
        'attendance_absent': attendance_absent,
        'total_subjects': total_subjects,
        'subject_data': subject_data,
    }
    return render(request, 'student_home_template.html', context)
def student_view_attendance(request):
   
    # Getting Logged in Student Data
    student = Students.objects.get(admin=request.user.id)
     
    # Getting Course Enrolled of LoggedIn Student
    course = student.course_id
     
    # Getting the Subjects of Course Enrolled
    subjects = Subjects.objects.filter(course_id=course)
    context = {
        "subjects": subjects
    }
    return render(request, "student/student_view_attendance.html", context)
 
def student_view_attendance_post(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('student_view_attendance')
    else:
        # Getting all the Input Data
        subject_id = request.POST.get('subject')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
 
        # Parsing the date data into Python object
        start_date_parse = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_parse = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
 
        # Getting all the Subject Data based on Selected Subject
        subject_obj = Subjects.objects.get(id=subject_id)
         
        # Getting Logged In User Data
        user_obj = CustomUser.objects.get(id=request.user.id)
         
        # Getting Student Data Based on Logged in Data
        stud_obj = Students.objects.get(admin=user_obj)
 
        # Now Accessing Attendance Data based on the Range of Date
        # Selected and Subject Selected
        attendance = Attendance.objects.filter(attendance_date__range=(start_date_parse,
                                                                       end_date_parse),
                                               subject_id=subject_obj)
        # Getting Attendance Report based on the attendance
        # details obtained above
        attendance_reports = AttendanceReport.objects.filter(attendance_id__in=attendance,
                                                             student_id=stud_obj)
 
        context = {
            "subject_obj": subject_obj,
            "attendance_reports": attendance_reports
        }
 
        return render(request, 'student_attendance_data.html', context)
 
def student_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('student_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        address = request.POST.get('address')
 
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
 
            student = Students.objects.get(admin=customuser.id)
            student.address = address
            student.save()
             
            messages.success(request, "Profile Updated Successfully")
            return redirect('student_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('student_profile')
 
def student_view_results(request):
    # Get the currently logged-in student
    student = Students.objects.get(user=request.user)

    # Get the student's results
    results = results.objects.filter(student=student)

    context = {
        'student': student,
        'results': results,
    }
    return render(request, 'student_view_results.html', context)
