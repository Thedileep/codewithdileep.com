from django.shortcuts import render, redirect,reverse
from django.contrib.auth import authenticate, login
from .models import AdmissionForm
from .backend import CustomAuthBackend
def pci(request):
    return render(request, 'index.html')
def admission_form_view(request):
    return render(request, 'admission_form.html')

def submit_admission_form(request):
    if request.method == 'POST':
        # Process the form data here
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        course = request.POST.get('course')
        country_state = request.POST['country_state']
        district = request.POST.get('district', '')
        pin = request.POST.get('pin', '')
        address = request.POST.get('address')

        # Save the form data to the database using the AdmissionForm model
        admission_form = AdmissionForm(
            first_name =first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            course=course,
            country_state=country_state,
            district=district,
            pin=pin,
            address=address
        )
        admission_form.save()

        return render(request, 'thank_you.html')

    # If the request method is not POST, simply render the admission form template
    return admission_form_view(request)
def show_form_details(request):
    # Retrieve all admission form data from the database
    admission_forms = AdmissionForm.objects.all()
    return render(request, 'form_details.html', {'admission_forms': admission_forms})

def login_view(request):
    if request.method == 'POST':
        # Get the username and password from the form submission
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            # User authentication successful, log in the user
            login(request, user)
            return redirect('index')  # Replace 'dashboard_view' with the URL name of your dashboard page
        else:
            # User authentication failed, show an error message or handle it accordingly
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})
    
    return render(request, 'login.html')