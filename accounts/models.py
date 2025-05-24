from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Create your models here.

class ProfileUser(AbstractUser):
    
    phone_regex = RegexValidator(
        regex=r'^01[0125][0-9]{8}$',
        message="Phone number must be a valid Egyptian number starting with 010, 011, 012, or 015"
    )
    mobile_phone = models.CharField(validators=[phone_regex], max_length=11, unique=True)

    
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    
    email_verified = models.BooleanField(default=False)


    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
