from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save,sender=User)
def profile_create(sender,instance,created,**kwargs):
    print('signals................')
    default_profile_pic='profile/THAR_BLACK_ygTzM9D.jpg'
    if created:
        profile=UserProfile.objects.create(user=instance,email=instance.email,first_name=instance.first_name,last_name=instance.last_name,profile_pic=default_profile_pic)
        