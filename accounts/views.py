from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth import login, logout, authenticate

# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("products")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form":form})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, 
                            username= username,
                            password= password
                            )
        if user is not None:
            login(request, user)
            return redirect("products")
        else:
            messages.error(request, "Invalid credentials")
    return render(request, "accounts/login.html")

def user_logout(request):
    logout(request)
    return redirect("login")