from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile, User

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        print('UserProfile created!')
    else: # when created is false means user already exist in database then update it
        try:
            profile=UserProfile.objects.get(user=instance) #it pass update data in user and it save
            profile.save()
            print('user is updated')

        
        except UserProfile.DoesNotExist: #except block exicute when userprofile is not exist 
            UserProfile.objects.create(user=instance) #user data goes on userprofile and it create automatically
            print('profile is not exist, but i created one')