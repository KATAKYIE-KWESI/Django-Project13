from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']

        if confirm_password == password:
            if User.objects.filter(username=username).exists():
                messages.error(request,'Username already exits')
            elif User.objects.filter(email=email).exists():
                messages.error(request,'Email already exists')
            else:
               user = User.objects.create_user(username=username,email=email,password=password)
               user.save()
               messages.success(request,'Account created successfully')
               return redirect('firstpage')

        return render(request,'register.html')

    else:
        return render(request,'register.html')


def firstpage(request):
     return render(request,'firstpage.html')

def log_in(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            user_obj= None

        if user_obj is not None:
            user = authenticate(username=user_obj.username,password=password)
            if user is not None:
                login(request,user)
                return redirect('firstpage')
            else:
                messages.error(request,'Incorrect password')

        else:
            messages.error(request,'User does not exist')

    return render(request,'register.html')

def log_out(request):
    logout(request)
    return redirect('register')







