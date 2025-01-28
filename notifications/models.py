from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('friend_request', 'Friend Request'),
        ('accepted_request', 'Accepted Friend Request'),
        ('new_post', 'New Post'),
        ('like', 'Like'),
        ('comment', 'Comment'),
    )

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    text = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        status = "Read" if self.is_read else "Unread"
        return f"Notification for {self.recipient.username}: {self.text} ({status})"
