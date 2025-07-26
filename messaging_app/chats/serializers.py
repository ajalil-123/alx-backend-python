
from rest_framework import serializers
from .models import CustomUser, Message, Conversation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['user_id', 'first_name', 'last_name', 'email']



class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(source= 'sender_id', read_only=True)
    class Meta:
         model = Message
         fields = ['message_id','sender','message_body', 'sent_at']
  


class ConversationSerializer(serializers.ModelSerializers):
    participants = UserSerializer(source='participants_id', many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True, source='message_set')  
    class Meta:
        model = Conversation
        fields = ['conversation_id','participants_id','created_at']



