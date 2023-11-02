from django.urls import path
from . import views

urlpatterns = [
    path('quiz/<int:quiz_id>/', views.quiz, name='quiz'),
    path('quiz_result/<int:quiz_id>/<int:score>/', views.quiz_result, name='quiz_result'),
]
