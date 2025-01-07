from django.shortcuts import render

# Create your views here.

def portfolio_view(request):
    return render(request, 'portfolio.html')