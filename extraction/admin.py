from django.contrib import admin
from .models import TextDetailing,EmailDetailing

@admin.register(TextDetailing)
class TextDetailingSavingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date_time')


@admin.register(EmailDetailing)
class EmailDetailingSavingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date_time')