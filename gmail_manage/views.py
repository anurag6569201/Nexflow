from django.shortcuts import render
from .models import GmailAccountDetails,GmailAccountLabelsCounts

from gmail_manage.gmail_auth.gmail_readonly_authentication import authenticate_gmail_for_readonly
from gmail_manage.gmail_actions import get_account_details_gmail_api,get_account_labels_gmail_api,get_gmail_data_at_intervals


from .forms import EmailIntervalForm
from django.utils.timezone import make_aware
from datetime import datetime
from django.http import JsonResponse

def refresh_gmail_data(request):
    gmail_detials_service=authenticate_gmail_for_readonly()
    get_account_details_gmail_api(request,gmail_detials_service)

    account_details, created = GmailAccountDetails.objects.get_or_create(user=request.user)
    return render(request, 'apps/gmail/partials/gmail_details.html', {'account_details': account_details})


def refresh_gmail_labels(request):
    gmail_labels_service=authenticate_gmail_for_readonly()
    get_account_labels_gmail_api(request,gmail_labels_service)

    account_labels_details, created = GmailAccountLabelsCounts.objects.get_or_create(user=request.user)
    label_info = account_labels_details.label_info or {} 
    return render(request, 'apps/gmail/partials/gmail_labels.html', {'account_labels_details': label_info})

def refresh_gmail_at_intervals(request):
    if request.method == "POST":
        start_time_str = request.POST.get('start_time')
        end_time_str = request.POST.get('end_time')

        try:
            # Parse datetime from strings
            start_time = datetime.fromisoformat(start_time_str)
            end_time = datetime.fromisoformat(end_time_str)

            # Authenticate and fetch emails
            gmail_intervals_service = authenticate_gmail_for_readonly()
            response_data = get_gmail_data_at_intervals(gmail_intervals_service, start_time, end_time)

            return JsonResponse(response_data, status=200)

        except ValueError:
            return JsonResponse({"errors": {"form": ["Invalid date format."]}}, status=400)
    else:
        return render(request, 'email/email_interval_form.html')

def gmail_manage(request):
    account_labels_details, created = GmailAccountLabelsCounts.objects.get_or_create(user=request.user)
    label_info = account_labels_details.label_info or {} 

    account_details, created = GmailAccountDetails.objects.get_or_create(user=request.user)

    context = {
        'account_details': account_details,
        'account_labels_details': label_info, 
    }
    
    return render(request, 'apps/gmail/gmail_manage.html', context)
