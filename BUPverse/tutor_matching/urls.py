from django.urls import path
from . import views

urlpatterns = [
    path('nextDoorposts_profile/', views.nextDoor_profile, name='nextDoor_profile'),
    path('nextDoorposts_homepage/', views.nextDoor_homepage, name='nextDoor_homepage'),
    path('nextDoorposts_tutor/', views.nextDoor_tutor_post_list, name='nextDoor_tutor_post_list'),
    path('nextDoorposts_student/', views.nextDoor_student_post_list, name='nextDoor_student_post_list'),
    path('nextDoorposts/create/', views.nextDoor_post_create, name='nextDoor_post_create'),
    path('nextDoorposts/details/<int:post_id>/', views.nextDoor_post_details, name='nextDoor_post_details'),
    path('nextDoorposts/edit/<int:post_id>/', views.nextDoor_post_edit, name='nextDoor_post_edit'),
    path('nextDoorposts/delete/<int:post_id>/', views.nextDoor_delete, name='nextDoor_delete'),
    path('nextDoorposts/nextDoor_matched_posts/<int:post_id>/', views.nextDoor_matched_posts, name='nextDoor_matched_posts'),
    
]
