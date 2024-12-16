from django.db import models
from django.contrib.auth.models import User

class AudioSaving(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    blob_url = models.FileField(upload_to='audio_files/', blank=True, null=True)
    is_transcribed = models.BooleanField(default=False)
    is_extracted = models.BooleanField(default=False)

    transcription_text = models.TextField(blank=True, null=True)
    date_time = models.DateTimeField(auto_now_add=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username if self.user else 'API User'}'s Audio File"
    
class TextDetailing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    text_detailing = models.ForeignKey(AudioSaving, on_delete=models.CASCADE, null=True, blank=True)
    output_text = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username if self.user else 'API User'}'s Text Detailing"