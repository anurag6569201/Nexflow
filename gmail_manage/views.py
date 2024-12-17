from django.shortcuts import render
from .models import GmailAccountDetails

def get_account_details_gmail_api():
    pass


def refresh_gmail_data(request):
    account_details, created = GmailAccountDetails.objects.get_or_create(primary_email=request.user.email)
    return render(request, 'apps/gmail/partials/gmail_details.html', {'account_details': account_details})


def gmail_manage(request):
    account_details,created=GmailAccountDetails.objects.get_or_create(primary_email=request.user.email)
    print(account_details)
    context={
        'account_details':account_details,
    }
    return render(request, 'apps/gmail/gmail_manage.html',context)