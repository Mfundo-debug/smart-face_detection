from django.db import models

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
    personal_email = models.EmailField(max_length=254)
    residential_address = models.CharField(max_length=200)
