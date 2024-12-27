from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('questionnaire/', questionnaire_view, name='questionnaire'),
]