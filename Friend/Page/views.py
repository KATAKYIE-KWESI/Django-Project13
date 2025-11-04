from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .forms import PostForm


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



@login_required
def upload_profile_pic(request):
    # Ensure the user has a profile (just in case)
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfilePicForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile picture updated successfully! Please refresh the page to see changes.")
            return redirect('upload_profile_pic')
        else:
            messages.error(request, "There was an error updating your profile picture.")
    else:
        form = ProfilePicForm(instance=profile)

    return render(request, 'Upload_profile.html', {'form': form})


from django.shortcuts import render, redirect
from .models import Post

def firstpage(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'firstpage.html', {'posts': posts})

def create_post(request):
    if request.method == 'POST':
        caption = request.POST.get('caption')
        image = request.FILES.get('image')
        Post.objects.create(user=request.user, caption=caption, image=image)
        return redirect('firstpage')
    return redirect('firstpage')



@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('firstpage')
    return render(request, 'confirm_delete.html', {'post': post})