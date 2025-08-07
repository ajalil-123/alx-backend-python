# messaging/models.py

from django.db import models
from django.contrib.auth.models import User
from .managers import UnreadMessagesManager

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)  # Track if message was edited
    edited_by = models.ForeignKey(User, related_name='edited_messages', null=True, blank=True, on_delete=models.SET_NULL)
    read = models.BooleanField(default=False)
    parent_message = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='replies',
        on_delete=models.CASCADE) 
    
    objects = models.Manager()  # Default manager
    unread = UnreadMessagesManager()  # ✅ Custom unread messages manager

    def __str__(self):
        return f"From {self.sender} to {self.receiver} - {self.timestamp}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user} - {self.message}"

class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='histories')
    old_content = models.TextField()
    edited = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History of Message ID {self.message.id} at {self.edited_at}"
