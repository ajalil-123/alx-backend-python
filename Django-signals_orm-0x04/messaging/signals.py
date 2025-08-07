
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification


# Signal receiver that runs after a Message is saved
@receiver(post_save, sender=Message)
def create_notification_on_message(sender,instance, created, **kwargs):
    if created : 
        # If a new message is created, generate a notification for the receiver
        Notification.objects.create(
            user=instance.receiver,
            message = instance
        )