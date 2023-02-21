from django.urls import path 
from . import views 

urlpatterns = [ 
    path('',views.user_post,name='user-post'),
    path('like-post/',views.post_like,name='post-like'),

]