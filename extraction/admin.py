from django.contrib import admin
from .models import TextDetailing

@admin.register(TextDetailing)
class TextDetailingSavingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date_time')