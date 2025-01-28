from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def notification_list(request):
    # Get all notifications
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    unread_count = notifications.filter(is_read=False).count()
    
    # Mark all as read when viewing
    if unread_count > 0:
        notifications.filter(is_read=False).update(is_read=True)
    
    return render(request, 'notifications/notification_list.html', {
        'notifications': notifications,
        'unread_count': unread_count
    })
