from django.shortcuts import render,redirect
from django.contrib.auth import login as auth_login
from django.contrib import messages
from .forms import RegisterForm

# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request,user)  # log in right after registering
            messages.success(request,"Welcome to BlogHub!")
            return redirect("post_list")
    else:
        form = RegisterForm()
    return render(request,"accounts/register.html",{"form": form})