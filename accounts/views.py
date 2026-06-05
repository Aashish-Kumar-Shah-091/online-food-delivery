from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.

def register(request):
    if request.method =="POST":
        form = RegisterForm(request.POST)

        if form.isvalid():
            user= form.save()
            login(request, user)

            messages.success = (request, "account created successfully")
            return redirect("home") 
        else:
            form = RegisterForm()

            return render(request, "accounts/registerhtml", {"form": form })
        
def login (request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password = password
        
        )

        if user:
            login(request, user)
            messages.success(request, "logged in successfully!")
            return redirect("home")
        

        messages.error(request, "invalid credentials ")

    return redirect("login.html")

@login_required
def profile_view(request):
    logout (request)
    messages.success(request, "logges out successfully!")
    return redirect("login")