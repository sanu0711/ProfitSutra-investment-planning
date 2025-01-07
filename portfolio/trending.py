from django.shortcuts import render

def trending_view(request):
    return render(request, 'trending.html')