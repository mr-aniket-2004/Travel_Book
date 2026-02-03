from django.shortcuts import render,redirect
from .forms import UserRegisterForm
from django.contrib.auth import login ,logout ,authenticate
from django.contrib import messages

from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings


# Create your views here.

def index(request):
    return render(request, 'index.html') 

def send_welcome_email(user):
    subject = 'Welcome to Travel Book 🎉'
    message = f'''
Hi {user.username},

Thanks for choosing Travel Book 🌍✈️
Your account has been created successfully.

Happy travelling!
Team Travel Book
'''
    from_email = settings.EMAIL_HOST_USER
    to_email = [user.email]

    send_mail(subject, message, from_email, to_email, fail_silently=False)


def UserLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('userlogin')
    return render(request, 'login.html')





def UserRegister(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messagess = f"Account is created Successfully {user.username}"
            if user.email:
                send_welcome_email(user)

            login(request, user)
            return render(request, 'Dashboard/dashboard.html', {
                'messagess': messagess
            })
        else:
            messagess = "Email already registered or password is weak"
            return render(request, 'signup.html', {
                'form': form,
                'messagess': messagess
            })
    else:
        form = UserRegisterForm()

    return render(request, 'signup.html', {'form': form})


