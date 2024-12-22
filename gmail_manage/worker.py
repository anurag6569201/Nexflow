import schedule
import time
from gmail_manage.gmail_actions import fetch_emails_in_interval_automatic
from gmail_manage.gmail_auth.gmail_readonly_authentication import authenticate_gmail_for_readonly
from datetime import datetime, timedelta
from extraction.gmail_data_extraction import process_and_save_gmail_detailing

def fetch_emails(request):
    now = datetime.now()
    formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
    print("Current time:", formatted_datetime)

    # Calculate start and end times using datetime objects
    start_time = now - timedelta(minutes=140)  # 10 minute ago
    end_time = now  # Current time

    # Format start and end times as strings
    formatted_start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
    formatted_end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")

    label = 'SENT'  # Change this to the desired label
    print("Start time:", formatted_start_time)
    print("End time:", formatted_end_time)
    print("Label:", label)


    # Authenticate and fetch emails
    gmail_intervals_service = authenticate_gmail_for_readonly()
    response_data = fetch_emails_in_interval_automatic(request,gmail_intervals_service, start_time, end_time,label)
    process_and_save_gmail_detailing(request,response_data)
    print(f"Fetched emails from {start_time} to {end_time}")

