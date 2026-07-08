from django.urls import path
from . import views

urlpatterns = [

    path('event_homepage/', views.event_homepage, name='event_homepage'),
     path('event_manage/', views.event_manage, name='event_manage'),
    path('events/create/', views.create_event, name='create_event'),
     path('event_post/', views.event_post_list, name='event_post_list'),
    path('events/<int:event_id>/', views.event_details, name='event_details'),
    path('events/edit/<int:event_id>/', views.edit_event, name='edit_event'),
    path('events/delete/<int:event_id>/', views.delete_event, name='delete_event'),
    path('routine/', views.view_routine, name='view_routine'),
    
    path('fix-conflicts/', views.fix_conflict, name='fix_conflict'),
    path('busy-slots/add/', views.add_busy_slot, name='add_busy_slot'),
    path('busy-slots/<int:slot_id>/edit/', views.edit_busy_slot, name='edit_busy_slot'),
    path('busy-slots/<int:slot_id>/delete/', views.delete_busy_slot, name='delete_busy_slot'),
    path('events/busy-slots/', views.add_busy_slot, name='add_busy_slot'),
    path('events/to-attend/', views.events_to_attend, name='events_to_attend'),
    path('events/update-routine/', views.update_routine, name='update_routine'),
    path('events/event_recom/', views.event_recom, name='event_recom'),
    path('events/my-events/', views.my_events, name='my_events'),\
     path('choose-number/', views.choose_number, name='choose_number'),


]