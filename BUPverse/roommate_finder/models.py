from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone

USER_TYPE_CHOICES = (
    ('looking_house', 'Looking for House'),
    ('looking_roommate', 'Looking for Roommates'),
)

GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'),
)

FOOD_TYPE = (
    ('self', 'Self Arrange'),
    ('shared', 'Shared Cooking (Schedule)'),
    ('helper', 'Combined Paid Helper'),
    ('Any','Any'),
)

  
ROOM_TYPE_CHOICES = (
    ('private', 'Private Room'),
    ('shared', 'Shared Room'),
    ('Any','Any'),

)

LOCATION_CHOICES = [
    ('Uttara East', 'Uttara East'),
    ('Uttara General Hospital', 'Uttara West'),
    ('Uttara Center, Tafalia Main Road, Uludaha, Baunia, Dhaka, Dhaka Metropolitan,1231', 'Uttara Center'),
    ('House Building', 'House Building (Uttara Hub)'),
    ('Azampur', 'Azampur (Uttara Link)'),
    ('Airport uttara', 'Airport (Hazrat Shahjalal)'),
    ('Abdullahpur, Uttara', 'Abdullahpur'),
    ('Diabari', 'Diabari'),
    ('Kamarpara', 'Kamarpara'),
    ('Khilkhet', 'Khilkhet (East of Airport)'),
    
    ('Tongi', 'Tongi'),
    ('Shyamoli', 'Shyamoli'),
    ('Agargaon', 'Agargaon'),
    ('Kafrul', 'Kafrul (West Agargaon)'),
    ('Kazipara', 'Kazipara (Near Mirpur 10)'),
    ('Shewrapara', 'Shewrapara (On Mirpur Road)'),
    ('Taltola', 'Taltola (Mirpur-Mohammadpur link)'),
    ('Pallabi', 'Pallabi'),
    ('Alubdi', 'Alubdi (Pallabi outskirts)'),
    ('Monipur', 'Monipur (School & Housing Area)'),
    ('Mirpur DOHS', 'Mirpur DOHS'),

    ('Mirpur 1', 'Mirpur Section 1'),
    ('Mirpur 2', 'Mirpur Section 2'),
    ('Mirpur 6', 'Mirpur Section 6'),
    ('Mirpur 10', 'Mirpur Section 10'),
    ('Mirpur 11', 'Mirpur Section 11'),
    ('Mirpur 12', 'Mirpur Section 12'),
    ('Mirpur 14', 'Mirpur 14 (Kalshi)'),

    ('Mohammadpur', 'Mohammadpur'),
    ('Dhanmondi', 'Dhanmondi'),
    ('Farmgate', 'Farmgate'),
]


DEPARTMENT_CHOICES = [
    ('Any', 'Any'),
    ('CSE', 'CSE'),
    ('ICT', 'ICT'),
    ('ES', 'Environmental Science'),
    ('ENG', 'English'),
    ('ECO', 'Economics'),
    ('IR', 'International Relations'),
    ('LAW', 'Law'),
    ('PA', 'Public Administration'),
    ('SOC', 'Sociology'),
    ('DS', 'Development Studies'),
    ('MCJ', 'Mass Communication & Journalism'),
    ('DMR', 'Disaster Management & Resilience'),
    ('PCHR', 'Peace, Conflict and Human Rights'),
    ('GEN', 'Business Administration - General'),
    ('AIS', 'Accounting & Information Systems'),
    ('MGT', 'Management Studies'),
    ('MKT', 'Marketing'),
    ('FNB', 'Finance & Banking'),
    ('BA/BSS', 'BA/BSS'),
]


class roomPost(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=16, choices=USER_TYPE_CHOICES)
    rent = models.PositiveIntegerField(help_text="Enter monthly rent")
    gender = models.CharField(max_length=10,choices=GENDER_CHOICES)
    food = models.CharField(max_length=20, choices=FOOD_TYPE)
    area = models.CharField(max_length=100, choices=LOCATION_CHOICES)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    phone_number = PhoneNumberField(blank=True, default='+880100000000')  
    move_in_date = models.DateField(default=timezone.now)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPE_CHOICES)
    full_address = models.TextField(blank=True, null=True, help_text="Write Address in detail")

    description = models.TextField(blank=True, null=True)

    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    dist_from_bup = models.FloatField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        name = self.user.get_full_name() or self.user.username
        return f'{name} | {self.created_at} | {self.area}'

