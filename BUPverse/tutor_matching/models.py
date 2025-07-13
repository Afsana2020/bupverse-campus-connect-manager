from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField



USER_TYPE_CHOICES = (
    ('looking_tutions', 'Looking for Tuitions'),
    ('looking_tutor', 'Looking for Tutors'),
)

GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'),
    ('any', 'Any'),
)

MEDIUM_CHOICES = (
    ('bangla', 'Bangla Version'),
    ('english', 'English Version'),
    ('english_mid', 'English Medium'),
    ('any', 'Any'),
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

    ('Adabar', 'Adabar'),
    ('Badda', 'Badda'),
    ('Bangsal', 'Bangsal'),
    ('Bashundhara', 'Bashundhara'),
    ('Cantonment', 'Cantonment'),
    ('Chawkbazar', 'Chawkbazar'),
    ('Dakshinkhan', 'Dakshinkhan'),
    ('Dhanmondi', 'Dhanmondi'),
    ('Gandaria', 'Gandaria'),
    ('Gulshan', 'Gulshan'),
    ('Hazaribagh', 'Hazaribagh'),
    ('Jatrabari', 'Jatrabari'),
    ('Kalabagan', 'Kalabagan'),
    ('Kamrangirchar', 'Kamrangirchar'),
    ('Khilgaon', 'Khilgaon'),
    ('Khilkhet', 'Khilkhet'),
    ('Kodomtoli', 'Kodomtoli'),
    ('Kotwali', 'Kotwali'),
    ('Lalbagh', 'Lalbagh'),
    ('Mirpur', 'Mirpur'),
    ('Mohammadpur', 'Mohammadpur'),
    ('Motijheel', 'Motijheel'),
    ('Mugda', 'Mugda'),
    ('New Market', 'New Market'),
    ('Paltan', 'Paltan'),
    ('Ramna', 'Ramna'),
    ('Rampura', 'Rampura'),
    ('Rupnagar', 'Rupnagar'),
    ('Sabujbagh', 'Sabujbagh'),
    ('Shah Ali', 'Shah Ali'),
    ('Shahbagh', 'Shahbagh'),
    ('Shahjahanpur', 'Shahjahanpur'),
    ('Shyampur', 'Shyampur'),
    ('Sutrapur', 'Sutrapur'),
    ('Tejgaon', 'Tejgaon'),
    ('Tejgaon Industrial Area', 'Tejgaon Industrial Area'),
    ('Turag', 'Turag'),
    ('Vatara', 'Vatara'),
]

CLASS_CHOICES = [
    ('1', 'Class 1'),
    ('2', 'Class 2'),
    ('3', 'Class 3'),
    ('4', 'Class 4'),
    ('5', 'Class 5'),
    ('6', 'Class 6'),
    ('7', 'Class 7'),
    ('8', 'Class 8'),
    ('SSC', 'SSC'),
    ('HSC', 'HSC'),
    ('Admission', 'Admission'),
    ('ANY', 'ANY'),
]

    

class nextDoorPost(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=16, choices=USER_TYPE_CHOICES)
    subjects = models.CharField(max_length=255)
    budget = models.IntegerField()
    medium = models.CharField(max_length=50,choices=MEDIUM_CHOICES)
    gender = models.CharField(max_length=10,choices=GENDER_CHOICES)
    location = models.CharField(max_length=100, choices=LOCATION_CHOICES)
    phone_number = PhoneNumberField(blank=True) 
    student_class = models.CharField(max_length=10, choices=CLASS_CHOICES)
    details = models.TextField(blank=True, null=True, help_text="Write any extra details")
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        student_name = self.user.get_full_name() or self.user.username
        return f'{student_name} | {self.subjects} | {self.location}'

