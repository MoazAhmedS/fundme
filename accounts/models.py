from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class ProfileUser(AbstractUser):
    phone_regex = RegexValidator(
        regex=r'^01[0125][0-9]{8}$',
        message="Phone number must be a valid Egyptian number starting with 010, 011, 012, or 015"
    )
    
    phone = models.CharField(validators=[phone_regex], max_length=11, unique=True)
    image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    facebook = models.URLField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    STATUS_CHOICES = [
        ('Student', 'Student'),
        ('Graduated', 'Graduated'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, blank=True, null=True)

    email_active = models.BooleanField(default=False)
    creat_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
