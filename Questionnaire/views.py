from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, 'home.html')

def questionnaire_view(request):
    if request.method == 'POST':
        messages.success(request, "Your responses have been recorded successfully!")
        return redirect('home')
    return render(request, 'questionnaire.html')