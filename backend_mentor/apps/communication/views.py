from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Message
from rest_framework import serializers

User = get_user_model()

class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.name', read_only=True)
    recipient_name = serializers.CharField(source='recipient.name', read_only=True)
    notification_text = serializers.CharField(source='get_notification_text', read_only=True)
    
    class Meta:
        model = Message
        fields = [
            'id', 'sender', 'sender_name', 'recipient', 'recipient_name',
            'message_type', 'content', 'is_read', 'created_at', 'read_at',
            'notification_text'
        ]
        read_only_fields = ['sender', 'created_at', 'read_at']

class MessageViewSet(viewsets.ModelViewSet):
    """ViewSet for managing messages between mentors and students"""
    
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        # Mentors see messages they sent
        if user.role == 'mentor':
            return Message.objects.filter(sender=user)
        
        # Students see messages they received
        elif user.role == 'student':
            return Message.objects.filter(recipient=user)
        
        return Message.objects.none()
    
    def perform_create(self, serializer):
        # Sender is automatically the logged-in user
        serializer.save(sender=self.request.user)
    
    @action(detail=False, methods=['get'])
    def unread(self, request):
        """Get unread messages for the current user"""
        if request.user.role != 'student':
            return Response(
                {'error': 'Only students can retrieve unread messages'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        messages = Message.objects.filter(
            recipient=request.user,
            is_read=False
        )
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark a message as read"""
        message = self.get_object()
        
        # Only recipient can mark as read
        if message.recipient != request.user:
            return Response(
                {'error': 'You can only mark your own messages as read'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        message.is_read = True
        message.read_at = timezone.now()
        message.save()
        
        serializer = self.get_serializer(message)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Mark all messages as read for the current user"""
        if request.user.role != 'student':
            return Response(
                {'error': 'Only students can mark messages as read'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        updated = Message.objects.filter(
            recipient=request.user,
            is_read=False
        ).update(is_read=True, read_at=timezone.now())
        
        return Response({
            'message': f'{updated} messages marked as read',
            'count': updated
        })
