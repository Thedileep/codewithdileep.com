from django import forms
from .models import Choice

class QuizForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text']
