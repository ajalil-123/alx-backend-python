
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('messages/', views.all_messages, name='all_messages'),
    path('delete-account/', views.delete_user, name='delete_user'),
     path('threads/', views.get_user_conversations, name='threaded_conversations'),
]
