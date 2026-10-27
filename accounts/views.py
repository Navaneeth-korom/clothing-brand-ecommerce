from django.shortcuts import render, redirect
from .forms import RegisterForm

# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("products")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form":form})