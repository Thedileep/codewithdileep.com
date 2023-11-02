from django.shortcuts import render, redirect
from .models import Quiz, Question, Choice
from .forms import QuizForm


def home(request):
    return render(request, 'home.html')

def quiz_result(request, quiz_id, score):
    quiz = Quiz.objects.get(pk=quiz_id)
    
    return render(request, 'quiz_result.html', {'quiz': quiz, 'score': score})

def quiz(request, quiz_id):
    quiz = Quiz.objects.get(pk=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    score = 0  # Initialize the user's score
    
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            for question in questions:
                # Get the user's selected choice ID for this question
                selected_choice_id = request.POST.get(f'question_{question.id}')
                
                # Get the correct choice for this question
                correct_choice = question.choice_set.get(is_correct=True)
                
                # Check if the selected choice is correct
                if selected_choice_id and int(selected_choice_id) == correct_choice.id:
                    score += 1  # Increment the score for correct answers

            # You can save the score in the user's profile or display it
            # depending on your application's requirements.

            # For simplicity, let's redirect to a result page with the score.
            return redirect('quiz_result', quiz_id=quiz_id, score=score)
    else:
        form = QuizForm()

    return render(request, 'quiz.html', {'quiz': quiz, 'questions': questions, 'form': form})
