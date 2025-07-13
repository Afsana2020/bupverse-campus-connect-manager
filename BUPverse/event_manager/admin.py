from django.contrib import admin
from django.utils import timezone
from .models import eventPost, UserRoutine, UserBusySlot


@admin.register(eventPost)
class EventPostAdmin(admin.ModelAdmin):
    list_display = (
        'event_title', 'user', 'date', 'start_time', 'end_time',
        'category', 'payment', 'is_expired_display'
    )
    search_fields = ('event_title', 'user__username', 'venue')
    list_filter = ('category', 'payment', 'date')

    def is_expired_display(self, obj):
        return obj.is_expired
    is_expired_display.boolean = True
    is_expired_display.short_description = 'Expired?'


@admin.register(UserRoutine)
class UserRoutineAdmin(admin.ModelAdmin):
    list_display = ('user', 'event_count')
    search_fields = ('user__username',)

    def event_count(self, obj):
        return obj.events.count()

@admin.register(UserBusySlot)
class UserBusySlotAdmin(admin.ModelAdmin):
    list_display = ('user', 'day_of_week', 'start_time', 'end_time')
    list_filter = ('day_of_week', 'user')
    search_fields = ('user__username',)
