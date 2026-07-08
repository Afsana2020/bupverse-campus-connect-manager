from django import forms
from tutor_matching.models import nextDoorPost



class nextDoorPostForm(forms.ModelForm):
    class Meta:
        model = nextDoorPost
        fields = [
            'user_type',
            'subjects',
            'budget',
            'medium',
            'gender',
            'student_class',
            'location',
            'phone_number',
            'details',
        ]



