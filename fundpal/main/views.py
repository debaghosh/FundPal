from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

def home(request):
    return render(request, 'main/home.html')

def register(request):
    context = {}
    return render(request, 'main/register.html', context)

def login(request):
    context = {}
    return render(request, 'main/login.html', context)