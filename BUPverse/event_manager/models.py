from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from datetime import datetime


EVENT_TYPE_CHOICES = [
    ('seminar', 'Seminar'),
    ('workshop', 'Workshop'),
    ('cultural', 'Cultural Program'),
    ('sports', 'Sports Event'),
    ('contest', 'Contest'),
]

PAID_CHOICES = [
    ('free', 'Free'),
    ('paid', 'Paid'),
]

EVENT_CATEGORY_CHOICES = [
    ('Tech', 'Tech'),
    ('Business', 'Business'),
    ('CP', 'Competitive programming'),
    ('Debate','Debate'),
    ('Hackathon','Hackathon'),
    ('CTF', 'Capture The Flag'),
    ('Cultural', 'Culture'),
    ('Career', 'Career / Skill'),
    ('Social', 'Social Work'),
    ('Research', 'Research / Academic'),
    ('Sports', 'Sports'),
    ('General', 'General'),
    ('Workshop', 'Workshop'),
    ('Others','Others'),
    ('',''),
]

DAYS_OF_WEEK = [
    (0, 'Monday'),
    (1, 'Tuesday'),
    (2, 'Wednesday'),
    (3, 'Thursday'),
    (4, 'Friday'),
    (5, 'Saturday'),
    (6, 'Sunday'),
]
NUMBER_CHOICES = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4 '),
    ('5', '5'),
    ('6', '6'),
     ('7', '7'),
      ('8', '8'),
       ('9', '9'),
        ('10', '10'),

]

class Recom(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    choose = models.CharField(max_length=10, choices=NUMBER_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Recommendation Preference"
        verbose_name_plural = "Recommendation Preferences"
        ordering = ['-created_at']


class eventPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_posts')
    event_type = models.CharField(max_length=16, choices=EVENT_TYPE_CHOICES)
    category = models.CharField(max_length=20, choices=EVENT_CATEGORY_CHOICES,default='')

    event_title = models.CharField(max_length=100, blank=True, null=True)
    theme = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def clean(self):
        super().clean()  
        if self.start_time >= self.end_time:
            raise ValidationError("End time must be after start time.")
        if hasattr(self, 'deadline') and self.deadline:  
            if self.deadline.date() > self.date:
                raise ValidationError("Registration deadline cannot be after the event date.")
    
    @property
    def is_expired(self):
        return self.date and self.date < timezone.now().date()
    
    def duration(self) -> float:
        start = timezone.make_aware(datetime.combine(self.date, self.start_time))
        end = timezone.make_aware(datetime.combine(self.date, self.end_time))
        return (end - start).total_seconds() / 3600

    venue = models.CharField(max_length=200)
    deadline = models.DateTimeField(help_text="Last date/time to register")
    registration_link = models.URLField(blank=True, null=True)

    payment = models.CharField(max_length=10, choices=PAID_CHOICES)
    contact_email = models.EmailField(blank=True, null=True)
    contact_number = PhoneNumberField(blank=True, null=True)

    poster = models.ImageField(upload_to='event_posters/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} | {self.event_title or "Untitled"} | {self.venue}'

    class Meta:
        ordering = ['date', 'start_time']

    
class UserRoutine(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    events = models.ManyToManyField(eventPost, through='UserEventSelection')

class UserEventSelection(models.Model):
    user_routine = models.ForeignKey(UserRoutine, on_delete=models.CASCADE)
    event = models.ForeignKey(eventPost, on_delete=models.CASCADE)
    importance_score = models.PositiveIntegerField(default=1)
    has_conflict = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('user_routine', 'event')
    
    @property
    def is_expired(self):
        return self.event.is_expired
    
class UserBusySlot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='busy_slots')
    task_name = models.CharField(max_length=100, blank=True)
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()

    

    def __str__(self):
        day_name = dict(DAYS_OF_WEEK).get(self.day_of_week, 'Unknown Day')
        return f"{self.user.username}'s busy time on {day_name} from {self.start_time} to {self.end_time}"
