from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib import messages
# from .chatbot import response_q
from .tests import chat_to_query

# Create your views here.
def home(request):
    # res = chat_to_query('top 10 stocks having highest marketcap')
    # print(res)
    return render(request, 'home.html')

def chatbot_view(request):
    # response = chat_to_query('top 10 stocks having highest marketcap')
    # response= response_q()
    # print(response)
    if request.method == 'POST':
        question = request.POST.get('question')
        if question:
            response = chat_to_query(question)
            return render(request, 'chatbot.html', {
                'response': response,
                'qus': question})
        else:
            messages.error(request, "Please enter a question to get response")
            return render(request, 'chatbot.html')    
    return render(request, 'chatbot.html')
  

def questionnaire_view(request):
    if request.method == 'POST':
        messages.success(request, "Your responses have been recorded successfully!")
        return redirect('home')
    return render(request, 'questionnaire.html')

