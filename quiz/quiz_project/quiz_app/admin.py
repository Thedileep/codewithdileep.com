from django.contrib import admin
from .models import Quiz, Question, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4

class QuestionInline(admin.TabularInline):
    model = Question
    inlines = [ChoiceInline]
    extra = 1

class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

# Register your models with the admin site
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question)
admin.site.register(Choice)
