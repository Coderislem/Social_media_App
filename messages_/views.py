from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Conversation, Message
from django.contrib.auth.models import User
from django.db.models import Q
from accounts.models import Profile
from friends.models import Friendship

@login_required
def conversations_list(request):
    conversations = Conversation.objects.filter(participants=request.user).order_by('-created_at')
    return render(request, 'messages/conversations.html', {'conversations': conversations})

@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    messages = conversation.messages.all().order_by('created_at')
    
    # Fix: Mark unread messages as read using correct filter syntax
    unread_messages = messages.filter(
        sender__isnull=False  # Make sure sender exists
    ).exclude(
        sender=request.user  # Exclude messages sent by current user
    ).filter(
        is_read=False  # Only unread messages
    )
    unread_messages.update(is_read=True)
    
    return render(request, 'messages/conversation.html', {
        'conversation': conversation,
        'messages': messages
    })

@login_required
def new_conversation(request):
    if request.method == 'POST':
        recipient_username = request.POST.get('recipient')
        recipient = get_object_or_404(User, username=recipient_username)
        
        # Check if conversation already exists
        existing_conv = Conversation.objects.filter(
            participants=request.user
        ).filter(
            participants=recipient
        ).first()
        
        if existing_conv:
            return redirect('conversation_detail', conversation_id=existing_conv.id)
            
        # Create new conversation
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, recipient)
        return redirect('conversation_detail', conversation_id=conversation.id)
        
    return render(request, 'messages/new_conversation.html')

@login_required
def send_message(request, conversation_id):
    if request.method == 'POST':
        conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
        content = request.POST.get('content')
        
        if content:
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content
            )
            
    return redirect('conversation_detail', conversation_id=conversation_id)

@login_required
def friends_messages(request):
    user_profile = request.user.profile
    # جلب جميع الأصدقاء
    friendships = Friendship.objects.filter(
        Q(profile1=user_profile) | Q(profile2=user_profile)
    )
    
    friends = []
    for friendship in friendships:
        if friendship.profile1 == user_profile:
            friends.append(friendship.profile2)
        else:
            friends.append(friendship.profile1)
            
    return render(request, 'messages/friends_messages.html', {'friends': friends})

@login_required
def start_conversation(request, friend_id):
    friend = get_object_or_404(Profile, id=friend_id)
    
    # البحث عن محادثة موجودة
    existing_conv = Conversation.objects.filter(
        participants=request.user
    ).filter(
        participants=friend.user
    ).first()
    
    if existing_conv:
        return redirect('conversation_detail', conversation_id=existing_conv.id)
        
    # إنشاء محادثة جديدة
    conversation = Conversation.objects.create()
    conversation.participants.add(request.user, friend.user)
    return redirect('conversation_detail', conversation_id=conversation.id)
