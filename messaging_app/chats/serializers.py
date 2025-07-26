
from rest_framework import serializers
from .models import CustomUser, Message


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['user_id', 'first_name', 'last_name', 'email']



class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model : Message
        fields : ['message_id','sender_id','message_body'] 


class ConversationSerializer(serializers.ModelSerializers):
    class Meta:
        model = Conversation
        fields = ['conversation_id','participants_id','created_at']