from django.db.models.signals import post_save
from django.dispatch import receiver
from friends.models import FriendRequest
from posts.models import Post, Like
from comments.models import Comment
from .models import Notification

@receiver(post_save, sender=FriendRequest)
def create_friend_request_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            recipient=instance.receiver.user,
            sender=instance.sender.user,
            notification_type='friend_request',
            text=f'{instance.sender.user.username} sent you a friend request'
        )

@receiver(post_save, sender=Like)
def create_like_notification(sender, instance, created, **kwargs):
    if created and instance.post.user != instance.user:
        Notification.objects.create(
            recipient=instance.post.user,
            sender=instance.user,
            notification_type='like',
            text=f'{instance.user.username} liked your post'
        )

@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created and instance.post.user != instance.user:
        Notification.objects.create(
            recipient=instance.post.user,
            sender=instance.user,
            notification_type='comment',
            text=f'{instance.user.username} commented on your post'
        )