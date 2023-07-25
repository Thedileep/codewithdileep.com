# backends.py
from django.contrib.auth.backends import BaseBackend
from .models import AdmissionForm
from datetime import datetime

class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            # Get the last two digits of the course number from the username
            last_two_digits = int(username[-2:])
            # Get the year as '20XX' where XX is the last two digits of the course number
            current_year = str(datetime.datetime.now().year)[-2:]
            year = f'20{last_two_digits:02}'

            # Check if the username follows the specified format
            if username[:2] == year and username[2:4].isdigit() and username[4:6].isdigit():
                # Combine the last two digits of the course number and the admission number
                course_number = int(username[2:4])
                admission_number = int(username[4:6])

                # Find the AdmissionForm with the matching course number and admission number
                admission_form = AdmissionForm.objects.get(course_number=course_number, admission_number=admission_number)

                # Check if the password matches the mobile number
                if admission_form.phone == password:
                    return admission_form.user

        except AdmissionForm.DoesNotExist:
            pass

        return None
