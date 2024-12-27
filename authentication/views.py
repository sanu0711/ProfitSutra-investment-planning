from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout

def sign_up(request):
    if request.method == 'POST':
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('sign_up')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use.")
            return redirect('sign_up')
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('sign_up')
        user = User.objects.create_user(
            username=username, 
            password=password1, 
            email=email, 
            first_name=fname, 
            last_name=lname
            )
        user.save()
        
        messages.success(request, "Your account has been created successfully!")
        return redirect('sign_in')  # Redirect to a success page, e.g., home

    return render(request, 'auth/sign_up.html')


def sign_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('chatbot')
        else:
            if not User.objects.filter(username=username).exists():
                messages.error(request, "User does not exist.")
            else:
                messages.error(request, "Incorrect password.")
            return redirect('sign_in')
    
    return render(request, 'auth/sign_in.html')

def sign_out(request):
    logout(request)
    messages.success(request, "You have logged out successfully!")
    return redirect('sign_in')