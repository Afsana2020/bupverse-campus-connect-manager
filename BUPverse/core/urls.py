from django.urls import path
from . import views as v1
from tutor_matching import views as v2
from roommate_finder import views as v3
from event_manager import views as v4

urlpatterns = [
    path('', v1.index, name='index'),
    path('profile_gen/', v1.general_profile, name='general_profile'),
    path('nextdoor/', v2.nextDoor_homepage, name='nextDoor_homepage'),
    path('roomate/', v3.room_homepage, name='room_homepage'),
    path('events/', v4.event_homepage, name='event_homepage'),
    path('about/', v1.about_us, name='about_us'),
    path('accounts/register/', v1.register, name='register'),
    path('profile/', v1.profile, name='profile'),
    path('profile/edit/', v1.profile_edit, name='profile_edit'),
    path('complete-profile/', v1.complete_profile, name='complete_profile'),

]


