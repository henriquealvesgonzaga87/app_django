from django.shortcuts import render
from core.models import Event


def list_events(request):
    user = request.user
    event = Event.objects.filter(user=user)
    datas = {'events': event}
    return render(request, 'agenda.html', datas)
