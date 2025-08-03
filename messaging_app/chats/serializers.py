from rest_framework import serializers
from .models import CustomUser, Conversation, Message
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    #sender = UserSerializer(source='sender_id', read_only=True)
    sender = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), read_only=False)
    class Meta:
        model = Message
        fields = ['message_id','conversation', 'sender', 'message_body', 'sent_at']


class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=CustomUser.objects.all()
    )
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']

    def get_messages(self, obj):
        messages = Message.objects.filter(conversation=obj)
        return MessageSerializer(messages, many=True).data

    def create(self, validated_data):
        participants = validated_data.pop('participants')
        conversation = Conversation.objects.create(**validated_data)
        conversation.participants.set(participants)
        return conversation


# Example of serializer using CharField and ValidationError
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered.")
        return value
