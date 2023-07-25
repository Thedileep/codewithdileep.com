from django.urls import path
from . import views

urlpatterns = [
     path('', views.pci, name='index'), 
      path('admission_form/', views.admission_form_view, name='admission_form_view'),
    path('submit-admission-form/', views.submit_admission_form, name='submit_admission_form'),
    path('form-details/', views.show_form_details, name='show_form_details'),
     path('login/', views.login_view, name='login_view'),
     #path('student_home/', StudentViews.student_home, name='student_home'),
    #path('student_view_results/', StudentViews.student_view_results, name='student_view_results'),
]