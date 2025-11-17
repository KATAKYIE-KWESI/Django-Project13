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


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Profile, FriendRequest
from .forms import ProfilePicForm
from django.contrib.auth.models import User
from .models import Post, FriendRequest
from .models import Notification

@login_required
def firstpage(request):
    posts = Post.objects.all().order_by('-created_at')
    users = User.objects.exclude(id=request.user.id)

    # Received friend requests
    friend_requests = request.user.received_requests.filter(status='pending')

    # Sent requests (to show status)
    sent_requests = FriendRequest.objects.filter(sender=request.user)

    # Notifications for current user
    notifications = Notification.objects.filter(sender=request.user, is_read=False).order_by('-created_at')
    unread_count = notifications.count()

    return render(request, 'firstpage.html', {
        'posts': posts,
        'users': users,
        'friend_requests': friend_requests,
        'sent_requests': sent_requests,
        'notifications': notifications,
        'unread_count': unread_count,
    })


@login_required
def send_request(request, user_id):
    receiver = get_object_or_404(User, id=user_id)
    if FriendRequest.objects.filter(sender=request.user, receiver=receiver, status='pending').exists():
        messages.warning(request, 'Friend request already sent.')
    else:
        FriendRequest.objects.create(sender=request.user, receiver=receiver)
        messages.success(request, f'Friend request sent to {receiver.username}')
    return redirect('firstpage')

from .models import Notification

#Accept and Decline with Notifications integrated

@login_required
def accept_request(request, request_id):
    fr = get_object_or_404(FriendRequest, id=request_id, receiver=request.user)
    fr.status = 'accepted'
    fr.save(update_fields=['status'])

    # Create notification for sender
    Notification.objects.create(
        sender=fr.sender,
        message=f"{request.user.username} accepted your friend request!"
    )

    messages.success(request, f'You are now friends with {fr.sender.username}')
    return redirect('firstpage')


@login_required
def decline_request(request, request_id):
    fr = get_object_or_404(FriendRequest, id=request_id, receiver=request.user)
    fr.status = 'declined'
    fr.save(update_fields=['status'])

    # Create notification for sender
    Notification.objects.create(
        sender=fr.sender,
        message=f"{request.user.username} declined your friend request."
    )

    messages.info(request, f'You declined friend request from {fr.sender.username}')
    return redirect('firstpage')


#Notifications view
@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(sender=request.user).order_by('-created_at')
    # Mark all as read when user opens page
    notifications.update(is_read=True)
    return render(request, 'notifications.html', {'notifications': notifications})
