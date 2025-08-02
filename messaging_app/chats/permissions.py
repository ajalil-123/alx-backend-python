
from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.participants.all()

class IsMessageSenderOrRecipient(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.sender or request.user == obj.recipient
    



class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    """

    def has_permission(self, request, view):
        # Only allow authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Allow only if the user is a participant of the conversation
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()

        # For Message objects, check if the user is part of the related conversation
        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()

        return False

