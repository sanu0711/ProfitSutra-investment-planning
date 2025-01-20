from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('questionnaire/', questionnaire_view, name='questionnaire'),
    path('chatbot/', chatbot_view, name='chatbot'),
    path('stock-research/', research_view, name='research_view'),
    path('questionnaire-history/', ques_history_view, name='ques_history_view'),
    path('questionnaire-history/<int:id>/', ques_explore, name='ques_explore'),
]