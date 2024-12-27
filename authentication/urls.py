from django.urls import path
from .views import *

urlpatterns = [
    path('login/',sign_in,name="sign_in"),
    path('signup/',sign_up,name="sign_up"),
    path('logout/', sign_out, name='sign_out'),
]