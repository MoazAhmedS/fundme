from allauth.socialaccount.signals import pre_social_login
from django.dispatch import receiver
import random

def generate_egyptian_phone_number():
    prefixes = ['010', '011', '012', '015']
    prefix = random.choice(prefixes)
    suffix = ''.join(str(random.randint(0, 9)) for _ in range(8))
    return prefix + suffix

@receiver(pre_social_login)
def populate_email_if_missing(sender, request, sociallogin, **kwargs):
    user = sociallogin.user
    if not user.email:
        user.email = f"{sociallogin.account.uid}@facebook.com"
        user.username = user.email  
        user.phone = generate_egyptian_phone_number()
    elif not user.phone:
        user.phone = generate_egyptian_phone_number()