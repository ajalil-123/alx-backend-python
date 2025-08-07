from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .models import Message, Notification

def home(request):
    return HttpResponse("Messaging app is running.")

def all_messages(request):
    messages = Message.objects.all()
    return HttpResponse("<br>".join([f"{m.sender} -> {m.receiver}: {m.content}" for m in messages]))


# messaging/views.py

from django.shortcuts import render, get_object_or_404
from .models import Message

def message_detail(request, message_id):
    message = get_object_or_404(Message, pk=message_id)
    history = message.history.all()
    return render(request, 'messaging/message_detail.html', {
        'message': message,
        'history': history
    })


from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import User

@login_required
def delete_user(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        return redirect('home')  # redirect to homepage or login page