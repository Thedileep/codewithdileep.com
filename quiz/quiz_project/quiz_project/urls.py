from django.contrib import admin
from django.urls import path, include
from quiz_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('quiz/', include('quiz_app.urls')),
]
