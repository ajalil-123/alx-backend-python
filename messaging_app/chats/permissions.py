
from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.participants.all()

class IsMessageSenderOrRecipient(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.sender or request.user == obj.recipient
    



from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    """

    def has_permission(self, request, view):
        # Allow only authenticated users to access the API
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Only participants can access/update/delete messages in a conversation
        if request.method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
            return request.user in obj.conversation.participants.all()
        return False
