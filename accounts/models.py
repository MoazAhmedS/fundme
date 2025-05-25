from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class ProfileUser(AbstractUser):
    phone_regex = RegexValidator(
        regex=r'^01[0125][0-9]{8}$', message="Phone number must be a valid Egyptian number starting with 010, 011, 012, or 015")
    
    phone = models.CharField( validators=[phone_regex],  max_length=11, unique=True, verbose_name="Phone Number"
    )
    image = models.ImageField(upload_to='profile_pics/',  blank=True, null=True, verbose_name="Profile Picture")
    
    birth_date = models.DateField(blank=True, null=True, verbose_name="Birth Date")
    facebook = models.URLField( max_length=255,  blank=True, null=True,verbose_name="Facebook Profile")
    country = models.CharField( max_length=100,   blank=True, null=True,verbose_name="Country")
    
    email_active = models.BooleanField(default=False, verbose_name="Email Activated")
    
    create_date = models.DateTimeField( auto_now_add=True,verbose_name="Creation Date")
    
    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"