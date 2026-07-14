
from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    subject = models.CharField(max_length=255)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # State tracking
    is_read = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False) 

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.subject} (From: {self.sender.username})"
