from django.db import models
from django.contrib.auth.models import User

class GmailAccountDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    primary_email = models.EmailField(default='example@gmail.com')
    total_messages = models.IntegerField(default=1000)
    total_threads = models.IntegerField(default=1000)