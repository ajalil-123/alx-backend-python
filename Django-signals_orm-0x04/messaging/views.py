from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .models import Message, Notification

def home(request):
    return HttpResponse("Messaging app is running.")

def all_messages(request):
    messages = Message.objects.all()
    return HttpResponse("<br>".join([f"{m.sender} -> {m.receiver}: {m.content}" for m in messages]))
