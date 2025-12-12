from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'recipient', 'message_type', 'is_read', 'created_at']
    list_filter = ['message_type', 'is_read', 'created_at']
    search_fields = ['sender__name', 'recipient__name', 'content']
    readonly_fields = ['created_at', 'read_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Message Info', {
            'fields': ('sender', 'recipient', 'message_type', 'content')
        }),
        ('Status', {
            'fields': ('is_read', 'created_at', 'read_at')
        }),
    )
