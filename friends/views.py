from django.shortcuts import render,redirect
from .models import FriendRequest,Friendship
from accounts.models import Profile
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from posts.models import Post
# Create your views here.

def profiles_view(request):
    profiles = Profile.objects.all()
    print(profiles)
    return render(request,"profiles.html",{"profiles":profiles})

def add_friend(request, reciver_id):
    reciver = get_object_or_404(Profile, id=reciver_id)
    user = request.user
    sender, created = Profile.objects.get_or_create(user=user)

    if sender == reciver:
        messages.error(request, "You cannot send a friend request to yourself!")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    if not FriendRequest.objects.filter(sender=sender, receiver=reciver).exists():
        try:
            FriendRequest.objects.create(sender=sender, receiver=reciver)
            messages.success(request, "Friend request sent successfully!")
        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
    else:
        messages.error(request, "Friend request already exists!")

    return redirect(request.META.get('HTTP_REFERER', '/'))

def FreindRequestSuggestions(request):
    current_profile = request.user.profile
    send_requests = FriendRequest.objects.filter(sender = current_profile).values_list('receiver_id',flat=True)
    receiver_requests = FriendRequest.objects.filter(receiver = current_profile).values_list('sender_id',flat=True)
    all_exculded_ids = list(send_requests) + list(receiver_requests)
    profile_suggestions = Profile.objects.exclude(id__in = all_exculded_ids).exclude(id = current_profile.id)
    return render(request,'profiles.html',{"profile_suggestions":profile_suggestions})
def Friends(request):
    profile = request.user.profile

    friends_1 = Friendship.objects.filter(profile1 = profile).values_list("profile2",flat=True)
    freinds_2 = Friendship.objects.filter(profile2 = profile).values_list("profile1",flat=True)
    friends_ids = list(friends_1) + list(freinds_2)
    friends_profile = Profile.objects.filter(id__in =friends_ids)
    return render(request,"friends.html",{"friends_profile":friends_profile})

def get_friend(request,id):
    friend = get_object_or_404(Profile,pk=id)
    current_profile = request.user.profile
    try:
        friend_ship = Friendship.objects.filter( Q(profile1 = current_profile , profile2 = friend) | Q(profile2 = current_profile,profile1 = friend))
        return friend_ship
    except Friendship.DoesNotExist:
        return None
def remove_friend(request,id):
    friend_ship = get_friend(request,id)
    friend_ship.delete()
    messages.success(request,"friend delete successfully !")
    return redirect(request.META.get('HTTP_REFERER', '/') )

@login_required
def people_list(request):
    # Get current user's profile
    user_profile = request.user.profile
    
    # Get all friendships where user is involved
    friendships = Friendship.objects.filter(
        Q(profile1=user_profile) | 
        Q(profile2=user_profile)
    )
    
    # Get friend profiles
    friend_profiles = set()
    for friendship in friendships:
        if friendship.profile1 == user_profile:
            friend_profiles.add(friendship.profile2)
        else:
            friend_profiles.add(friendship.profile1)
            
    # Get sent friend requests
    sent_requests = FriendRequest.objects.filter(sender=user_profile).values_list('receiver', flat=True)
    
    # Get all profiles except friends and self
    people = Profile.objects.exclude(
        id__in=[p.id for p in friend_profiles]
    ).exclude(
        id=user_profile.id
    ).exclude(
        id__in=sent_requests
    )
    
    return render(request, 'people.html', {'people': people})

@login_required
def user_profile(request, profile_id):
    # Get profile directly using ID
    profile = get_object_or_404(Profile, id=profile_id)
    user = profile.user
    posts = Post.objects.filter(user=user).order_by('-created_at')
    
    # Get user's friends
    friendships = Friendship.objects.filter(
        Q(profile1=profile) | Q(profile2=profile)
    )
    friends = []
    for friendship in friendships:
        if friendship.profile1 == profile:
            friends.append(friendship.profile2)
        else:
            friends.append(friendship.profile1)
    
    print(f"Debug - Profile ID: {profile_id}")
    print(f"Debug - Profile: {profile}")
    print(f"Debug - Posts count: {posts.count()}")
    print(f"Debug - Friends count: {len(friends)}")
    
    context = {
        'profile': profile,
        'posts': posts,
        'friends': friends
    }
    
    # Change template path to match your directory structure
    return render(request, 'profile.html', context)
