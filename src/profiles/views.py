from django.shortcuts import render
from .models import Profile,Relationship
from .forms import ProfileForm

# Views Start from here ----------------X
def user_profile(request):
    profile = Profile.objects.get(user= request.user) 
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile) 
    confirm = False 

    if request.method == 'POST': 
        if form.is_valid():
            form.save()
            confirm = True 

    context = {
        'form': form,
        'profile': profile,
        'confirm': confirm,
        
    }
    return render(request,'profiles/user_profile.html',context)  

def receive_invitation(request):
    profile = Profile.objects.get(user=request.user)
    qs = Relationship.objects.invitation_received(profile) 

    context = {
        'qs': qs,
    }
    return render(request,'profiles/my_invite.html',context) 


def profile_list(request):
    user = request.user 
    qs = Profile.objects.get_all_profiles(user)

    context = {
        'qs':qs,
    }
    return render(request,'profiles/all_profiles.html',context) 

def send_envitation(request):
    user = request.user 
    qs = Profile.objects.get_all_profiles_for_sent_invite(user)
    context = {
        'qs':qs,
    }
    return render(request,'profiles/send_invitation.html',context) 
