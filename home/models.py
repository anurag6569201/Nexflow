from django.db import models
from django.contrib.auth.models import User


class AudioSaving(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    audio_file = models.FileField(upload_to='audio_files/')
    date_time = models.DateTimeField(auto_now_add=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username if self.user else 'API User'}'s Audio File"
