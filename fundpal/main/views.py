from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import requests
import json

def home(request):
    return render(request, 'main/home.html')

def register(request):
    form = RegisterForm()
    if request.method=='POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account was created for ' + form.cleaned_data.get('username'))
            return redirect('login')

    context = {'form':form}
    return render(request, 'main/register.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        cap_token = request.POST.get('g-recaptcha-response')
        
        cap_url = "https://www.google.com/recaptcha/api/siteverify"
        cap_secret = "6LdhKdIZAAAAAAiJ42ywngqbCAacEqtgmI-e_IPc"
        cap_dict = {'secret': cap_secret,'response':cap_token}
        cap_server_response = requests.post(url=cap_url, data=cap_dict)
        cap_json = json.loads(cap_server_response.text)
        if cap_json["success"]==False:
            messages.error(request, 'Captcha incorrect. Try again')
            return render(request, 'main/login.html')

        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect')
            return render(request, 'main/login.html')
        
    context = {}
    return render(request, 'main/login.html', context)


def logoutPage(request):
    logout(request)
    return redirect('home')