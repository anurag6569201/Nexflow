from django.contrib import admin
from .models import AudioSaving


@admin.register(AudioSaving)
class AudioSavingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'audio_file', 'date_time', 'uploaded_at')


