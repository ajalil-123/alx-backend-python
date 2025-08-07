from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .models import Message, Notification

def home(request):
    return HttpResponse("Messaging app is running.")

def all_messages(request):
    messages = Message.objects.all()
    return HttpResponse("<br>".join([f"{m.sender} -> {m.receiver}: {m.content}" for m in messages]))




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
    

from django.shortcuts import render
from .models import Message


def get_user_conversations(request):
    if not request.user.is_authenticated:
        # Redirect or handle anonymous user
        return render(request, 'messaging/threaded_conversations.html', {'threads': []})

    # Optimize by selecting related foreign keys and prefetching replies
    messages = Message.objects.filter(
        sender=request.user,  
        parent_message__isnull=True  # Only top-level threads
    ).select_related(
        'receiver'  # Avoid extra queries when accessing receiver
    ).prefetch_related(
        'replies__sender',  # Avoid extra queries when accessing replies and their senders
        'replies__receiver'
    ).order_by('-timestamp')

    return render(request, 'messaging/threaded_conversations.html', {
        'threads': messages
    })


from django.shortcuts import render
from .models import Message

def inbox_unread_messages(request):
    if not request.user.is_authenticated:
        return render(request, 'messaging/inbox.html', {'messages': []})

    # Using custom manager with optimized query
    unread_messages = Message.unread.unread_for_user(request.user).only(
        'id', 'sender', 'receiver', 'timestamp', 'content'
    )

    return render(request, 'messaging/inbox.html', {
        'messages': unread_messages
    })

