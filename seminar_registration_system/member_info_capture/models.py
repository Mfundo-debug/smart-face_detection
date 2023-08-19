from django.db import models
import requests
import random, string, time
from datetime import date
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.db import IntegrityError
import uuid
def validate_email(value):
    if '@' not in value:
        raise ValidationError('Invalid email address.')

def validate_address(value):
    #check if the address is valid using Google Maps API
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + value + '&key=' + 'AIzaSyD-9tSrke72PouQMnMX-a7eZSW0jkFMBWY'
    params = {'address': value, 'key': 'AIzaSyD-9tSrke72PouQMnMX-a7eZSW0jkFMBWY'}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise ValidationError('Invalid address.')
    result = response.json()
    if result['status'] != 'OK':
        raise ValidationError('Invalid address.')

def generate_system_email(last_name, first_names):
    #generate initials from first names
    initials = ''.join([name[0] for name in first_names.split()])
    #generate the email address
    email = f'{last_name}{initials}@SmartSystem.com'
    #check if the email address already exists in the database
    count = 0
    while Member.objects.filter(system_email=email).exists():
        #generate a new email address
        count += 1
        email = f'{last_name}{initials}{count:02}@SmartSystem.com'
    return email

def validate_id_number(id_number):
    #check if the ID number is of South African type
    if len(id_number) != 13 or not id_number.isdigit():
        return None, None, None, None, None
    #extract the date of birth from the ID number
    year = int(id_number[0:2])
    month = int(id_number[2:4])
    day = int(id_number[4:6])
    if year < 22:
        year += 2000
    else:
        year += 1900
    dob = date(year, month, day)
    #calculate the age from the date of birth
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    #extract the gender from ID number
    gender = 'Male' if int(id_number[6:10]) < 5000 else 'Female'
    #extract the nationality from the ID number
    nationality = 'South African'
    #Extract the country from the ID number
    country_code = int(id_number[10:12])
    countries = {
        0: 'South African',
        1: 'Zimbabwean',
        2: 'Mozambican',
        3: 'Lesotho',
        4: 'Swaziland',
        5: 'Botswana',
        6: 'Namibia',
        7: 'Zambian',
        8: 'Nigerian',
        9: 'Malawi',

    }
    country = countries.get(country_code, 'Unknown')
    return id_number, age, gender, nationality, country

class Member(models.Model):
    NEW_STUDENT = 'new'
    RETURNING_STUDENT = 'returning'
    STUDENT_TYPE_CHOICES = [
        (NEW_STUDENT, 'New Student'),
        (RETURNING_STUDENT, 'Returning Student'),
    ]
    student_type = models.CharField(
        max_length=20,
        choices=STUDENT_TYPE_CHOICES,
        default=NEW_STUDENT,
    )

    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    personal_email = models.EmailField(max_length=254, validators=[validate_email])
    residential_address = models.CharField(max_length=200 )
    system_email =  models.EmailField(max_length=254, null=False, unique=True)
    id_number = models.CharField(max_length=13, null=False, default='default_value', validators=[validate_id_number])
    user_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def save(self, *args, **kwargs):
        #generate the system email address if it does not exist
        if not self.system_email:
            self.system_email = generate_system_email(self.last_name, self.first_name)
        #check if the system email address already exists in the database
        while True:
            try:
                super().save(*args, **kwargs)
                break
            except IntegrityError:
                self.system_email = generate_system_email(self.last_name, self.first_name)
                self.pk = None

        # Validate the ID number and extract the student's information
        id_number = self.id_number.strip()
        if len(id_number) == 13 and id_number.isdigit():
            # The ID number is of South African type
            year = int(id_number[0:2])
            month = int(id_number[2:4])
            day = int(id_number[4:6])
            if year < 22:
                year += 2000
            else:
                year += 1900
            dob = date(year, month, day)
            today = date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            gender = 'Male' if int(id_number[6:10]) < 5000 else 'Female'
            nationality = 'South African'
            country_code = int(id_number[10:12])
            countries = {
                0: 'South African',
                1: 'Swaziland',
                2: 'Botswana',
                3: 'Lesotho',
                4: 'Namibia',
                5: 'Zimbabwe',
                6: 'Nigeria',
                7: 'Other',
                8: 'Other',
                9: 'Other',
            }
            country = countries.get(country_code, 'Unknown')
            self.age = age
            self.gender = gender
            self.nationality = nationality
            self.country = country
        else:
            # The ID number is not of South African type
            self.age = None
            self.gender = None
            self.nationality = None
            self.country = None
            self.id_number = None
            self.save_manual_info = True
        super().save(*args, **kwargs)