from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm  # Updated form names
from django.contrib.auth import login, logout
from django.views.generic.edit import FormView
from django.views.generic import CreateView
from .models import Profile
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from posts.views import Profile_posts
# Create your views here.

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            return redirect('post_list')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required  
def home_view(request):
    return render(request, 'home.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def profile(request):
    posts = Profile_posts(request, request.user.id)
    profile_info = Profile.objects.get(user=request.user)

    return render(request, "profile.html", {"posts": posts, "profile_info": profile_info})

from django.urls import reverse

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register_1.html', {'form': form})

