from django.shortcuts import render
from .models import GmailAccountDetails,GmailAccountLabelsCounts

from gmail_manage.gmail_auth.gmail_readonly_authentication import authenticate_gmail_for_readonly
from gmail_manage.gmail_auth.gmail_modify_authentication import authenticate_gmail_for_modify
from gmail_manage.gmail_actions import get_account_details_gmail_api,get_account_labels_gmail_api,get_gmail_data_at_intervals,delete_emails_efficiently_by_labels,fetch_emails_from_sender,move_emails_to_trash


from datetime import datetime
from django.http import JsonResponse

import schedule
import time
from gmail_manage.worker import fetch_emails

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


def delete_gmail_by_labels(request):
    if request.method == "POST":
        label = request.POST.get('label')
        max_emails = int(request.POST.get('max_emails', 0))
        order_by = request.POST.get('order_by', 'oldest')
        no_of_days = int(request.POST.get('no_of_days', 30))

        try:
            gmail_delete_service = authenticate_gmail_for_modify()
            response_logs = delete_emails_efficiently_by_labels(
                gmail_delete_service, label, max_emails, order_by, no_of_days
            )
            return JsonResponse({"success": True, "logs": response_logs}, status=200)
        except ValueError as e:
            return JsonResponse({"success": False, "errors": [str(e)]}, status=400)
        except Exception as e:
            return JsonResponse({"success": False, "errors": ["An unexpected error occurred."]}, status=500)
    else:
        return render(request, 'email/email_interval_form.html')


def delete_gmail_by_id(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            gmail_delete_service_by_id = authenticate_gmail_for_modify()
            
            email_ids = fetch_emails_from_sender(gmail_delete_service_by_id, email)
            move_emails_to_trash(gmail_delete_service_by_id, email_ids)
            
            return JsonResponse({"status": "success", "message": f"{len(email_ids)} emails deleted successfully."})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return render(request, "delete_emails.html")




def gmail_manage(request):
    account_labels_details, created = GmailAccountLabelsCounts.objects.get_or_create(user=request.user)
    label_info = account_labels_details.label_info or {} 

    account_details, created = GmailAccountDetails.objects.get_or_create(user=request.user)

    context = {
        'account_details': account_details,
        'account_labels_details': label_info, 
    }
    
    return render(request, 'apps/gmail/gmail_manage.html', context)



def testing(request):
    schedule.every(1).minutes.do(fetch_emails)

    print("Scheduler started. Fetching emails every 10 minutes...")
    while True:
        schedule.run_pending()
        time.sleep(1)