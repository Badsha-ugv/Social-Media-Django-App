from django.shortcuts import render,redirect
from .models import Post ,Like,Comment 
from profiles.models import Profile
from .forms import PostForm,CommentForm


# my views start from here 
def user_post(request):
    post = Post.objects.all()
    profile = Profile.objects.get(user=request.user)

    # post form  
    post_form = PostForm() 
    comment_form = CommentForm() 

    add_post = False

    if 'post_form_submit' in request.POST:
        post_form = PostForm(request.POST , request.FILES) 
        if post_form.is_valid():
            instance = post_form.save(commit=False)
            instance.author = profile
            instance.save() 
            post_form = PostForm()
            add_post = True
            
    if 'comment_form_submit' in request.POST:
        comment_form = CommentForm(request.POST ) 
        if comment_form.is_valid():
            instance = comment_form.save(commit=False)
            instance.user = profile 
            instance.post = Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            comment_form = CommentForm() 



    context = {
        'post': post,
        'profile': profile,
        'post_form': post_form,
        'comment_form': comment_form,
        'add_post': add_post,
    }
    return render(request,'posts/main.html', context) 

def post_like(request):
    user = request.user 
    if request.method == 'POST':
        post_id = request.POST.get('post_id') 
        post_obj = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user) 

        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile) 
        
        like,created = Like.objects.get_or_create(user=profile,post_id=post_id) 
        if not created:
            if like.value == 'like':
                like.value = 'unlike' 
            else:
                like.value = 'like'
        else:
            like.value = 'like'
            
        post_obj.save()
        like.save() 
    return redirect('user-post')



