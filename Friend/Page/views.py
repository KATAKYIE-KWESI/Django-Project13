from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import ProfilePicForm
from .models import Profile  # ✅ import the model (not the module)


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        confirm_password = request.POST['confirm_password']

        if not email or not password or not confirm_password or not username:
            messages.error(request, 'All fields are required')

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, 'Account created successfully')
                return redirect('firstpage')
        else:
            messages.error(request, 'Passwords do not match')

    return render(request, 'register.html')


def firstpage(request):
    return render(request, 'firstpage.html')


def log_in(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, 'Email and/or Password is required')
            return redirect('register')

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            user_obj = None

        if user_obj is not None:
            user = authenticate(request, username=user_obj.username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('firstpage')
            else:
                messages.error(request, 'Incorrect password.')
                return render(request, 'register.html')
        else:
            messages.error(request, 'No user found with this email.')
            return render(request, 'register.html')

    return render(request, 'register.html')


def log_out(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('register')

from django.shortcuts import render, redirect
from .forms import ProfilePicForm

def upload_profile_pic(request):
    if request.method == 'POST':
        form = ProfilePicForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('upload_profile_pic')
    else:
        form = ProfilePicForm(instance=request.user.profile)

    return render(request, 'Upload_profile.html', {'form': form})  # ✅ correct filename
