from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'department', 'phone_number')
    list_filter = ('department', 'degree')
    search_fields = ('user__username', 'full_name', 'phone_number')
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'full_name', 'phone_number', 'is_complete')
        }),
        ('Academic Info', {
            'fields': ('department', 'semester', 'degree')
        }),
        ('Other Info', {
            'fields': ('linkedin', 'facebook', 'additional_info', 'pic'),
            'classes': ('collapse',)  
        }),
    )