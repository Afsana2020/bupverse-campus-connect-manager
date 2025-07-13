from django import forms
from roommate_finder.models import roomPost
from django import forms
from django.utils.safestring import mark_safe
from .models import roomPost

class roomPostForm(forms.ModelForm):
    class Meta:
        model = roomPost
        fields = [
            'user_type',
            'rent',
            'gender',
            'food',
            'area',
            'department',
            'phone_number',
            'move_in_date',
            'room_type',
            'full_address',
            'description',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if field.help_text:
                field.help_text = mark_safe(f'<small class="form-text text-muted">{field.help_text}</small>')
