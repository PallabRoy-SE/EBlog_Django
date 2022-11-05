from django.shortcuts import render, HttpResponse, redirect
from datetime import datetime
from home.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate

# Create your views here.
def index(request):
    if request.user.is_anonymous:
        # Do something for authenticated users.
        return redirect('/signin')
    return render(request, 'index.html', {"name": request.user.username})


def about(request):
    return render(request, 'about.html', {"name": request.user.username})

def services(request):
    return render(request, 'services.html', {"name": request.user.username})

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        contact = Contact(name=name, email=email, phone=phone, desc=desc, date=datetime.now())
        contact.save()
        messages.success(request, 'Your message has been sent sucsessfully!')

    return render(request, 'contact.html', {"name": request.user.username})

def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # A backend authenticated the credentials
            return redirect('/')
        else:
            # No backend authenticated the credentials
            return render(request, 'signin.html')
    return render(request, 'signin.html')

def signout(request):
    logout(request)
    return redirect('/signin')

def register(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.create_user(name, email, password)
        login(request, user)
        messages.success(request, 'Your account has been created sucsessfully!')
        return redirect('/')
    else:
        return render(request, 'register.html')