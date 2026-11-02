from django.shortcuts import render, redirect
from products.forms import ContactForm
from django.contrib import messages

def home(request):
    return render(request, "home.html")

def contact_us(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been submitted.")
            return redirect("contact_us")
    else:
        form = ContactForm()
    return render(request, "contact.html", {"form":form})