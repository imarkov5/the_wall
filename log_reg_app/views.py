from django.shortcuts import render, redirect
import bcrypt
from django.contrib import messages
from .models import *


def index(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.validator(request.POST)
    
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    hashed_password = bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt()).decode()
    new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], birthday=request.POST['birthday'], email=request.POST['email'], password = hashed_password)
    request.session['name'] = new_user.first_name
    request.session['id'] = new_user.id
    request.session['message'] = "You have successfully registered!"
    return redirect('/wall')

def login(request):
    logged_user = User.objects.filter(email=request.POST['email'])
    if len(logged_user) > 0:
        logged_user = logged_user[0]
        if bcrypt.checkpw(request.POST['pw'].encode(), logged_user.password.encode()):
            request.session['name'] = logged_user.first_name
            request.session['id'] = logged_user.id
            request.session['message'] = "You have successfully logged in!"
            return redirect('/wall')
        else:
            messages.error(request, "Wrong password!")
            return redirect('/')
    else:
        messages.error(request, "Wrong email!")
        return redirect('/')

