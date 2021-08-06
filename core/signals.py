from django.db.models.signals import post_save
from core.models import UserProfile
from django.contrib.auth import get_user_model


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=get_user_model())