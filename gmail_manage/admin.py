from django.contrib import admin
from .models import GmailAccountDetails,GmailAccountLabelsCounts,GmailWholeData

@admin.register(GmailAccountDetails)
class TextDetailingSavingAdmin(admin.ModelAdmin):
    list_display = ('primary_email', 'total_messages', 'total_threads')


admin.site.register(GmailAccountLabelsCounts)
admin.site.register(GmailWholeData)