from django.shortcuts import render, redirect
from core.models import Event
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime, timedelta
from django.http.response import Http404, JsonResponse
from django.contrib.auth.models import User


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
    current_date = datetime.now() - timedelta(hours=1) # shows the events of the day till 1 hour late
    event = Event.objects.filter(user=user, event_date__gt=current_date)  # shows only the events further than current day
    datas = {'events': event}
    return render(request, 'agenda.html', datas)


@login_required(login_url='/login/')
def event(request):
    id_event = request.GET.get('id')
    datas = {}
    if id_event:
        datas['event'] = Event.objects.get(id=id_event)
    return render(request, 'event.html', datas)


@login_required(login_url='/login/')
def submit_event(request):
    if request.POST:
        title = request.POST.get('title'),
        for pos in title:
            title = pos
        event_date = request.POST.get('event_date'),
        for pos in event_date:
            event_date = pos
        description = request.POST.get('description'),
        for pos in description:
            description = pos
        user = request.user
        id_event = request.POST.get('id_event')
        if id_event:
            event = Event.objects.get(id=id_event)
            if event.user == user:
                event.title = title
                event.description = description
                event.event_date = event_date
                event.save()
            # Event.objects.filter(id=id_event).update(title=title, event_date=str(event_date), description=description)
        else:
            Event.objects.create(title=title, event_date=str(event_date), description=description, user=user)

    return redirect('/')


@login_required(login_url='/login/')
def delete_event(request, id_event):
    user = request.user
    try:
        event = Event.objects.get(id=id_event)
    except Exception:
        raise Http404
    if user == event.user:
        event.delete()
    else:
        raise Http404()
    return redirect('/')


def json_list_events(request, id_user):
    user = User.objects.get(id=id_user)
    event = Event.objects.filter(user=user).values('id', 'title')
    return JsonResponse(list(event), safe=False)
