from django.contrib import admin
from .models import AudioSaving,TextDetailing


@admin.register(AudioSaving)
class AudioSavingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'blob_url', 'date_time', 'uploaded_at')



@admin.register(TextDetailing)
class TextDetailingSavingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date_time')

