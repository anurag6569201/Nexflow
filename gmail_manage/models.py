from django.db import models

class GmailAccountDetails(models.Model):
    primary_email = models.EmailField(default='example@gmail.com')
    total_messages = models.IntegerField(default=1000)
    total_threads = models.IntegerField(default=1000)