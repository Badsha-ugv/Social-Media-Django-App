from django.urls import path 
from . import views 


urlpatterns = [
    path('',views.user_profile,name='user-profile'),
    path('my-invitation/',views.receive_invitation,name='my-invitation'),
    path('all-profile/',views.profile_list,name='all-profile'),
    path('send-invitation/',views.send_envitation,name='send-invitation'),



]