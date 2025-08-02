
from rest_framework import permissions

class IsParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.participants.all()

class IsMessageSenderOrRecipient(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.sender or request.user == obj.recipient
