from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

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


SEMESTER_CHOICES=[
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    ('5','5'),
    ('6','6'),
    ('7','7'),
    ('8','8'),
]

degree_choices = [('BSc', 'Bachelor of Science'), ('MSc', 'Master of Science')]


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    semester = models.CharField(max_length=2, choices=SEMESTER_CHOICES)
    degree = models.CharField(max_length=3, choices=degree_choices)
    phone_number = PhoneNumberField(blank=True, null=True) 
    linkedin = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)
    pic = models.ImageField(upload_to='user_pic/', blank=True, null=True)
    is_complete = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.user.username}'s Profile"