from django.shortcuts import render,redirect, get_object_or_404
from .models import FriendRequest,Friendship
from accounts.models import Profile
from django.contrib.auth.models import User
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
    user_profile = request.user.profile
    
    # Get friend requests
    received_requests = FriendRequest.objects.filter(
        receiver=user_profile,
        accepted=False
    ).select_related('sender')
    
    # Original people suggestions logic
    friendships = Friendship.objects.filter(
        Q(profile1=user_profile) | 
        Q(profile2=user_profile)
    )
    
    friend_profiles = set()
    for friendship in friendships:
        if friendship.profile1 == user_profile:
            friend_profiles.add(friendship.profile2)
        else:
            friend_profiles.add(friendship.profile1)
            
    sent_requests = FriendRequest.objects.filter(sender=user_profile).values_list('receiver', flat=True)
    
    people = Profile.objects.exclude(
        id__in=[p.id for p in friend_profiles]
    ).exclude(
        id=user_profile.id
    ).exclude(
        id__in=sent_requests
    )
    
    return render(request, 'people.html', {
        'people': people,
        'friend_requests': received_requests,
        'friends':friend_profiles
    })

@login_required
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile
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
            
    return render(request, 'profile.html', {
        'profile': profile,
        'posts': posts,
        'friends': friends
    })


def my_profile(request):
    profile = request.user.profile
    posts = Post.objects.filter(user = request.user)
    friendships = Friendship.objects.filter(
        Q(profile1=profile) | Q(profile2=profile)
    )
    friends = []
    for friendship in friendships:
        if friendship.profile1 == profile:
            friends.append(friendship.profile2)
        else:
            friends.append(friendship.profile1)
    return render(request,'profile.html',{
        'profile':profile,
        'posts':posts,
        'friends':friends
    })


















@login_required
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, receiver=request.user.profile)
    
    if request.method == 'POST':
        # Create friendship
        Friendship.objects.create(
            profile1=friend_request.sender,
            profile2=friend_request.receiver
        )
        
        # Mark request as accepted
        friend_request.accepted = True
        friend_request.save()
        
        messages.success(request, f'You are now friends with {friend_request.sender.user.username}')
        return redirect('people_list')

@login_required
def reject_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, receiver=request.user.profile)
    
    if request.method == 'POST':
        friend_request.delete()
        messages.info(request, f'Friend request from {friend_request.sender.user.username} rejected')
        return redirect('people_list')

@login_required
def search_profiles(request):
    query = request.GET.get('q')
    profiles = Profile.objects.filter(
        Q(user__username__icontains=query) |
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query)
    ) if query else []
    
    return render(request, 'search_results.html', {'profiles': profiles, 'query': query})
# @login_required
# def friends(request):
#     profile = request.user.profile
#     friendshipts = Friendship.objects.filter(Q(profile1 = profile) or Q(profile2=profile))
#     friends = []
#     for friendshipt in friendshipts:
#         if friendshipt.profile1 == profile:
#             friends.append(friendshipt.profile2)
#         elif friendshipt.profile2 == profile:
#             friends.append(friendshipt.profile1)
#     return render(request,)
