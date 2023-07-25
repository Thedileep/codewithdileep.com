# models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

username = get_user_model()
class AdmissionForm(models.Model):
    first_name= models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, default='')
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    course = models.CharField(max_length=100)
    country_state= models.CharField(max_length=100, default='')
    district = models.CharField(max_length=100, default='')       
    pin = models.CharField(max_length=10, default='')
    address= models.TextField(blank=True, null=True)
    user = models.OneToOneField(username, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name

class SessionYearModel(models.Model):
	id = models.AutoField(primary_key=True)
	session_start_year = models.DateField()
	session_end_year = models.DateField()
	objects = models.Manager()
# Overriding the Default Django Auth
# User and adding One More Field (user_type)
class CustomUser(AbstractUser):
	HOD = '1'
	STAFF = '2'
	STUDENT = '3'
	
	EMAIL_TO_USER_TYPE_MAP = {
		'hod': HOD,
		'staff': STAFF,
		'student': STUDENT
	}

	user_type_data = ((HOD, "HOD"), (STAFF, "Staff"), (STUDENT, "Student"))
	user_type = models.CharField(default=1, choices=user_type_data, max_length=10)
class Courses(models.Model):
	id = models.AutoField(primary_key=True)
	course_name = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = models.Manager()
class Students(models.Model):
	id = models.AutoField(primary_key=True)
	admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
	gender = models.CharField(max_length=50)
	profile_pic = models.FileField()
	address = models.TextField()
	course_id = models.ForeignKey(Courses, on_delete=models.DO_NOTHING, default=1)
	session_year_id = models.ForeignKey(SessionYearModel, null=True,
										on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = models.Manager()
	
class AdminHOD(models.Model):
	id = models.AutoField(primary_key=True)
	admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = models.Manager()

class Staffs(models.Model):
	id = models.AutoField(primary_key=True)
	admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
	address = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = models.Manager()

class Subjects(models.Model):
	id =models.AutoField(primary_key=True)
	subject_name = models.CharField(max_length=255)
	
	# need to give default course
	course_id = models.ForeignKey(Courses, on_delete=models.CASCADE, default=1)
	staff_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = models.Manager()

class Attendance(models.Model):

	# Subject Attendance
	id = models.AutoField(primary_key=True)
	subject_id = models.ForeignKey(Subjects, on_delete=models.DO_NOTHING)
	attendance_date = models.DateField()
	session_year_id = models.ForeignKey(SessionYearModel, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = models.Manager()

class AttendanceReport(models.Model):
	# Individual Student Attendance
	id = models.AutoField(primary_key=True)
	student_id = models.ForeignKey(Students, on_delete=models.DO_NOTHING)
	attendance_id = models.ForeignKey(Attendance, on_delete=models.CASCADE)
	status = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = models.Manager()

class NotificationStudent(models.Model):
	id = models.AutoField(primary_key=True)
	student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
	message = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = models.Manager()

class NotificationStaffs(models.Model):
	id = models.AutoField(primary_key=True)
	staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
	message = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = models.Manager()

class StudentResult(models.Model):
	id = models.AutoField(primary_key=True)
	student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
	subject_id = models.ForeignKey(Subjects, on_delete=models.CASCADE, default=1)
	subject_exam_marks = models.FloatField(default=0)
	subject_assignment_marks = models.FloatField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = models.Manager()

#Creating Django Signals
@receiver(post_save, sender=CustomUser)

# Now Creating a Function which will
# automatically insert data in HOD, Staff or Student
def create_user_profile(sender, instance, created, **kwargs):
	# if Created is true (Means Data Inserted)
	if created:
	
		# Check the user_type and insert the data in respective tables
		if instance.user_type == 1:
			AdminHOD.objects.create(admin=instance)
		if instance.user_type == 2:
			Staffs.objects.create(admin=instance)
		if instance.user_type == 3:
			Students.objects.create(admin=instance,
									course_id=Courses.objects.get(id=1),
									session_year_id=SessionYearModel.objects.get(id=1),
									address="",
									profile_pic="",
									gender="")

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
	if instance.user_type == 1:
		instance.AdminHod.save()
	if instance.user_type == 2:
		instance.staffs.save()
	if instance.user_type == 3:
		instance.students.save()

