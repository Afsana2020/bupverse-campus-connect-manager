from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile
from phonenumber_field.formfields import PhoneNumberField

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ProfileForm(forms.ModelForm):
    phone_number = PhoneNumberField(
        widget=forms.TextInput(attrs={'placeholder': '+8801XXXXXXXXX'}),
        required=True
    )
    
    class Meta:
        model = UserProfile
        fields = [
            'full_name',
            'department',
            'semester', 
            'degree',
            'phone_number',
            'linkedin',
            'facebook',
            'additional_info',
            'pic',
            
        ]
        