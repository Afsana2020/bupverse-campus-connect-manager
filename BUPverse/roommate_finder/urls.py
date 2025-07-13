from django.urls import path
from . import views

urlpatterns = [
    path('room_profile/', views.room_profile, name='room_profile'),
    path('room_homepage/', views.room_homepage, name='room_homepage'),
    path('roommate-posts/', views.roommate_post_list, name='roommate_post_list'),
    path('house-posts/', views.house_post_list, name='house_post_list'),
    path('post/<int:post_id>/', views.room_post_details, name='room_post_details'),
    path('post/create/', views.room_post_create, name='room_post_create'),
    path('post/edit/<int:post_id>/', views.room_post_edit, name='room_post_edit'),
    path('post/delete/<int:post_id>/', views.room_delete, name='room_delete'),
    path('matches/<int:post_id>/', views.room_matched_posts, name='room_matched_posts'),
]

