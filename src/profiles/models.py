from django.db import models
from django.contrib.auth.models import User
# from django.utils.text import slugify 
from django.template.defaultfilters import slugify 
from .utils import get_random_code
# Create your models here.

class Profile(models.Model):
    first_name = models.CharField(max_length=100,blank=True)
    last_name = models.CharField(max_length=100,blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default='no bio.')
    email = models.EmailField(max_length=200,blank=True)
    country = models.CharField(max_length=100,blank=True)
    avatar = models.ImageField(upload_to='user_avatar/', default='user.png') 
    friends = models.ManyToManyField(User,blank=True,related_name='friends')
    slug = models.SlugField(unique=True, blank=True) 
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True) 


    def get_friends(self):
        return self.friends.all() 
    
    def get_friends_number(self):
        return self.friends.all().count() 
    
    def get_post_number(self):
        return self.posts.all().count()  
    
    def get_all_post(self):
        return self.posts.all() 
    
    def get_likes_given(self):
        likes = self.like_set.all() 
        total_like = 0 
        for item in likes:
            if item.value == 'like':
                total_like += 1 
        return total_like 
    
    def get_likes_received(self):
        posts = self.posts.all() 
        total_like = 0  
        for item in posts:
            total_like = item.liked.all().count() 
        return total_like 
    
    

    def save(self, *args, **kwargs):
        ex = False 
        if self.first_name and self.last_name:
            to_slug = slugify(str(self.first_name) + " "+str(self.last_name)) 
            ex = Profile.objects.filter(slug=to_slug).exists() 
            while ex:
                to_slug = slugify(to_slug +" "+str(get_random_code()))
                ex = Profile.objects.filter(slug=to_slug).exists() 
        else:
            to_slug = str(self.user)
        self.slug = to_slug 
        # super().save(*args, **kwargs) 
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.created.strftime('%d-%m-%Y')}" 
    
RELATION_STATUS = (
    ('send','send'),
    ('accepted','accepted'),
)
class Relationship(models.Model):
    sender = models.ForeignKey(Profile, related_name="sender",on_delete=models.CASCADE)
    receiver = models.ForeignKey(Profile, related_name="receiver",on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=RELATION_STATUS) 

    def __str__(self):
        return f"{self.sender}  - {self.receiver} - {self.status}" 
    

