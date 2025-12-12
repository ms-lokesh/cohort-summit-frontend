from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Message(models.Model):
    """Messages sent from mentors to students"""
    
    MESSAGE_TYPES = [
        ('general', 'General'),
        ('completion', 'Completion'),
        ('pending', 'Pending Review'),
    ]
    
    sender = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='sent_messages',
        limit_choices_to={'role': 'mentor'}
    )
    recipient = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='received_messages',
        limit_choices_to={'role': 'student'}
    )
    message_type = models.CharField(
        max_length=20, 
        choices=MESSAGE_TYPES, 
        default='general'
    )
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', '-created_at']),
            models.Index(fields=['sender', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.sender.name} to {self.recipient.name} - {self.message_type}"
    
    def get_notification_text(self):
        """Get notification text based on message type"""
        type_texts = {
            'general': 'New message from your mentor',
            'completion': 'Task completed! Check your progress',
            'pending': 'You have pending items to review',
        }
        return type_texts.get(self.message_type, 'New notification')
