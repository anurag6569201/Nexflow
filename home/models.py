from django.db import models
from django.contrib.auth.models import User

class UserProfileREADME(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, default="")  # Markdown content
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s README"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    bio = models.CharField(max_length=50)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
    background_picture = models.ImageField(upload_to='profile_background/', blank=True)

    address=models.CharField(max_length=100)
    insta=models.CharField(max_length=100)
    github=models.CharField(max_length=100)
    linkedin=models.CharField(max_length=100)
    twitter=models.CharField(max_length=100)
    website=models.CharField(max_length=100)

    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.user.username}'s Profile"


    