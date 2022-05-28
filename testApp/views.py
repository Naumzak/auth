from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def login_users(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse(f'{username} logged')
        else:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            return HttpResponse(f'{username} created')


@login_required(login_url='/loginu')
def logout_users(request):
    if request.method == 'GET':
        return render(request, 'logout.html')
    else:
        logout(request)
