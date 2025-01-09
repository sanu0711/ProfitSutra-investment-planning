

from django.urls import path
from . import views
from .trending import trending_view 

urlpatterns = [
    path('', views.portfolio_view, name='portfolio'),
    path('update_create_portfolio/', views.update_create_portfolio, name='update_create_portfolio'),
    path('trending/', trending_view, name='trending'),
]
