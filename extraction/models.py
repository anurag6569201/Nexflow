from django.db import models
from django.contrib.auth.models import User
from home.models import AudioSaving

class TextDetailing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    text_detailing = models.ForeignKey(AudioSaving, on_delete=models.CASCADE, null=True, blank=True)
    output_text = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username if self.user else 'API User'}'s Text Detailing"