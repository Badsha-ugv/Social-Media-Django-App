from django.shortcuts import render,redirect, get_object_or_404
from .models import Profile,Relationship
from .forms import ProfileForm
from django.db.models import Q
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
    print(qs) 
    results = list(map(lambda x: x.sender,qs)) 
    print(results) 
    is_empty = False 
    if len(results) == 0:
        is_empty = True 

    context = {
        'qs': results,
        'is_empty': is_empty
    }
    return render(request,'profiles/my_invite.html',context) 



def send_envitation(request):
    user = request.user 
    qs = Profile.objects.get_all_profiles_for_sent_invite(user)
    context = {
        'qs':qs,
    }
    return render(request,'profiles/send_invitation.html',context) 

def accept_invite(request):
    if request.method == 'POST': 
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user = request.user) 
        rel = get_object_or_404(Relationship,sender=sender,receiver=receiver) 
        if rel.status == 'send':
            rel.status = 'accepted'
            rel.save()
    return redirect('my-invitation') 


def reject_invite(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        rel.delete() 
    return redirect('my-invitation')

def profile_list(request):
    user = request.user 
    qs = Profile.objects.get_all_profiles(user)

    context = {
        'qs':qs,
    }
    return render(request,'profiles/all_profiles.html',context) 

from django.views.generic import ListView 
from django.contrib.auth.models import User 

class ProfileListView(ListView):
    model = Profile
    template_name = 'profiles/all_profiles.html'
    # context_object_name = 'qs'

    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user)
        return qs 
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        user  = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user) 
        context['profile'] = profile

        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receive = []
        rel_send = []

        for item in rel_r.all():
            rel_receive.append(item.receiver.user)
            
        for item in rel_s.all():
            rel_send.append(item.sender.user)
        
        context['rel_send'] = rel_send
        context['rel_receive'] = rel_receive

        context['is_empty'] = False
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True


        return context 


def send_invitation(request):
    if request.method == 'POST': 
        pk = request.POST.get('profile_pk') 
        user = request.user 
        sender = Profile.objects.get(user=user) 
        receiver= Profile.objects.get(pk=pk) 

        rel = Relationship.objects.create(sender=sender, receiver=receiver,status="send")

        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('user-profile')


def remove_friend(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
            )
        print(rel)
        rel.delete() 
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('user-profile')
