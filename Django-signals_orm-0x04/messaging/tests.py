from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class MessagingSignalTestCase(TestCase):
    def setUp(self):
        # Create two users for testing
        self.sender = User.objects.create_user(username='jalil', password='password')
        self.receiver = User.objects.create_user(username='kudus', password='password')

    def test_notification_created_on_message_send(self):
        # Send a message from sender to receiver
        Message.objects.create(sender=self.sender, receiver=self.receiver, content='Hi Kudus!')

        # Check that a notification was created
        self.assertEqual(Notification.objects.count(), 1)

        # Check that the notification belongs to the correct user
        notification = Notification.objects.first()
        self.assertEqual(notification.user, self.receiver)
