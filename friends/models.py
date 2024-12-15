from django.db import models
from django.contrib.auth.models import User
from accounts.models import Profile
class FriendRequest(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sent_requests')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='received_requests')
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self):
        status = "Accepted" if self.accepted else "Pending"
        return f"FriendRequest from {self.sender.first_name} to {self.receiver.first_name} ({status})"

class Friendship(models.Model):
    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friends1')
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friends2')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('profile1', 'profile2')

    def __str__(self):
        return f"Friendship between {self.profile1.first_name} and {self.profile2.first_name}"
