# chats/models.py
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest')
    created_at = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=128)
    
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return self.username
    

class Conversation(models.Model):
    conversation_id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False)
    participants_id = models.ForeignKey(CustomUser,on_delete=models.CASCADE, to_field='user_id',
        related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)



class Message (models.Model):
    message_id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False )
    sender_id = models.ForeignKey(CustomUser,on_delete=models.CASCADE, to_field="user_id",related_name="messages")
    message_body = models.TextField(null=False, blank=False)
    sent_at = models.DateTimeField(auto_now_add=True)