from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import eventPost, UserRoutine, UserEventSelection, UserBusySlot,Recom
from event_manager.utils.event_code import SimpleScheduler

class EventPostForm(forms.ModelForm):
    class Meta:
        model = eventPost
        fields = [
            'event_title', 'event_type', 'category', 'theme',
            'date', 'start_time', 'end_time', 'venue', 'deadline',
            'description', 'poster', 'payment', 'registration_link',
            'contact_email', 'contact_number'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        deadline = cleaned_data.get('deadline')
        date = cleaned_data.get('date')

        if start_time and end_time and start_time >= end_time:
            raise ValidationError("Event end time must be after start time.")

        if deadline and date and deadline.date() > date:
            raise ValidationError("Registration deadline cannot be after the event date.")

        return cleaned_data
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None) 
        super().__init__(*args, **kwargs)


class UserBusySlotForm(forms.ModelForm):
    class Meta:
        model = UserBusySlot
        fields = ['task_name', 'day_of_week', 'start_time', 'end_time']
        widgets = {
            'task_name': forms.TextInput(attrs={
                'placeholder': 'e.g., Math Class, Work Shift',
                'class': 'form-control'
            }),
            'day_of_week': forms.Select(attrs={'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
            'end_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
        }
        labels = {
            'task_name': 'Task Name',
            'day_of_week': 'Day',
            'start_time': 'Start Time',
            'end_time': 'End Time',
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        day_of_week = cleaned_data.get('day_of_week')

        if not all([start_time, end_time, day_of_week]):
            raise ValidationError("All fields are required.")

        if start_time >= end_time:
            raise ValidationError("End time must be after start time.")
        
        return cleaned_data
class UserEventSelectionForm(forms.ModelForm):
    class Meta:
        model = UserEventSelection
        fields = ['event', 'importance_score']
        widgets = {
            'importance_score': forms.NumberInput(attrs={'min': 1, 'max': 10}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user:
            # Only show events that match user's categories and aren't expired
            self.fields['event'].queryset = eventPost.objects.filter(
                category__in=self.user.event_categories.all(),
                deadline__gte=timezone.now()
            ).exclude(user=self.user)  # Exclude events they created

    def clean(self):
        cleaned_data = super().clean()
        event = cleaned_data.get('event')
        
        if self.user and event:
            # Check if event is already in routine
            routine = UserRoutine.objects.get(user=self.user)
            if UserEventSelection.objects.filter(
                user_routine=routine,
                event=event
            ).exclude(pk=self.instance.pk).exists():
                raise ValidationError("This event is already in your routine.")
            
            # Check for time conflicts
            scheduler = SimpleScheduler(self.user)
            if not scheduler.check_availability(
                event.date, event.start_time, event.end_time
            ):
                raise ValidationError("This event conflicts with your existing schedule.")
        
        return cleaned_data
    

class RecomForm(forms.ModelForm):
    class Meta:
        model = Recom
        fields = ['choose']
        labels = {
            'choose': "How many hours do you want to spend on events this week?",
        }
        widgets = {
            'choose': forms.Select(attrs={'class': 'form-select'}),
        }