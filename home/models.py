from django.db import models
from django.contrib.auth.models import User

class AudioSaving(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    blob_url = models.FileField(upload_to='audio_files/')
    file_blog_uri = models.CharField(max_length=500, blank=True, null=True)
    audio_file_name = models.CharField(max_length=255, blank=True, null=True)

    base_64_string = models.TextField(blank=True, null=True)
    is_transcribed = models.BooleanField(default=False)
    transcription_text = models.TextField(blank=True, null=True)
    

    date_time = models.DateTimeField(auto_now_add=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username if self.user else 'API User'}'s Audio File"



class audio_recordings(models.Model):
    
