# messaging/signals.py

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:  # Check if this is an update
        try:
            original = Message.objects.get(pk=instance.pk)
            if original.content != instance.content:
                # Log the old content
                MessageHistory.objects.create(
                    message=original,
                    old_content=original.content
                )
                instance.edited = True
        except Message.DoesNotExist:
            pass



# messaging/signals.py

from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, MessageHistory, Notification

@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    # Explicitly delete messages where the user was sender or receiver
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete message histories related to the user's messages
    MessageHistory.objects.filter(message__sender=instance).delete()
    MessageHistory.objects.filter(message__receiver=instance).delete()

    # Delete notifications related to the user
    Notification.objects.filter(user=instance).delete()

    print(f"Cleaned up messages, histories, and notifications for user: {instance.username}")
