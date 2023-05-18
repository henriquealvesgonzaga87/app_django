from django.shortcuts import render, redirect
from core.models import Event
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def login_user(request):
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('/')


def submit_login(request):
    if request.POST:
        username = request.POST.get('username')  # take the username from html input
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'User or password invalid!')
    return redirect('/')


@login_required(login_url='/login/')
def list_events(request):
    user = request.user
    event = Event.objects.filter(user=user)
    datas = {'events': event}
    return render(request, 'agenda.html', datas)
