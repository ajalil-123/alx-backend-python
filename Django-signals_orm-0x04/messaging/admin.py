from django.contrib import admin
from .models import Message, Notification

# Register models so they are manageable via Django admin interface
admin.site.register(Message)
admin.site.register(Notification)
