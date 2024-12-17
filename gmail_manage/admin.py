from django.contrib import admin
from .models import GmailAccountDetails

@admin.register(GmailAccountDetails)
class TextDetailingSavingAdmin(admin.ModelAdmin):
    list_display = ('primary_email', 'total_messages', 'total_threads')

