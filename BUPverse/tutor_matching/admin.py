from django.contrib import admin
from .models import nextDoorPost


@admin.register(nextDoorPost)
class nextDoorPostAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'subjects', 'medium','budget', 'location','latitude','longitude','phone_number','student_class','details')
    search_fields = ('user__username', 'subjects', 'location')
    list_filter = ('subjects', 'medium', 'gender', 'location')

    def name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    name.short_description = 'Name'

    def time_slot(self, obj):
        return f"{obj.get_preferred_day_display()} at {obj.preferred_start_time.strftime('%I:%M %p')}"
    time_slot.short_description = 'Preferred Time Slot'


