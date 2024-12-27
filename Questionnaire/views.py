from django.shortcuts import render
# Create your views here.
def home(request):
    return render(request, 'home.html')

def questionnaire_view(request):
    return render(request, 'questionnaire.html')