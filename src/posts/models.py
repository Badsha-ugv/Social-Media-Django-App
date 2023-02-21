from django.db import models
from django.core.validators import FileExtensionValidator
from profiles.models import Profile 

# my models start from here -------------x-----------
class Post(models.Model):
    content = models.TextField(blank=True)
    image = models.ImageField(blank=True, upload_to='post_image/',validators= [FileExtensionValidator(['png', 'jpg', 'jpeg','webp'])])
    liked = models.ManyToManyField(Profile, blank=True, related_name='likes')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name='posts') 
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def number_of_likes(self):
        return self.liked.all().count() 
    
    def number_of_comment(self):
        return self.comment_set.all().count() 
    
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return str(self.content[:20]) 
    

class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE) 
    body = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return str(self.pk) 

LIKE_VALUE = (
    ('like','like'),
    ('unlike','unlike'),
)
class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)             
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(max_length=10, choices= LIKE_VALUE) 
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.user} - {self.post} - {self.value}" 