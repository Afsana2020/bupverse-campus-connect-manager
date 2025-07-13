from django.contrib import admin
from .models import roomPost

@admin.register(roomPost)
class roomPostAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'area', 'rent', 'gender','department','dist_from_bup', 'longitude','latitude')
    search_fields = ('user__username', 'area', 'full_address')
    list_filter = ('user_type', 'gender', 'area')
