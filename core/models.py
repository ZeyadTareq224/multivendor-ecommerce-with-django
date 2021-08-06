from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USERNAME_FIELD = 'email'
    email = models.EmailField(blank=False, unique=True)
    REQUIRED_FIELDS = []

    def get_username(self):
        return self.email.split("@")[0]

    def get_profile(self):
        return self.userprofile_set.all()[0]

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_vendor = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.get_username()}-Profile"
