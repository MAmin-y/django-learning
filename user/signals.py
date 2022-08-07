from django.contrib.auth.models import User
from .models import Profile

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


#@receiver(post_save, sender=Profile)                              in ye ravesh bara connect kardane
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(
            user = instance,
            username= instance.username,
            email=instance.email,
            name=instance.first_name,
        )

def delete_user(sender, instance, **kwargs):
    user = instance.user
    user.delete()


def update_user(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()

post_save.connect(create_profile, sender= User)               #in ham ye ravaesh digast
post_save.connect(update_user, sender= Profile)               #in ham ye ravaesh digast
post_delete.connect(delete_user, sender= Profile)