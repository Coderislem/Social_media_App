from django.shortcuts import render,redirect
from .models import FriendRequest,Friendship
from accounts.models import Profile
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db.models import Q
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
