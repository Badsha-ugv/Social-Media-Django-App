from django.shortcuts import render
from .models import Profile
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

