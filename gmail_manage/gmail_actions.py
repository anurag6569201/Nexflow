from googleapiclient.errors import HttpError
from gmail_manage.models import GmailAccountDetails,GmailAccountLabelsCounts

def get_account_details_gmail_api(request,service):
    """Fetch general details about the Gmail account."""
    try:
        profile = service.users().getProfile(userId='me').execute()
        account_details,created=GmailAccountDetails.objects.get_or_create(user=request.user)
        account_details.primary_email=profile.get('emailAddress')
        account_details.total_messages=profile.get('messagesTotal')
        account_details.total_threads=profile.get('threadsTotal')
        account_details.save()

    except HttpError as error:
        print(f"An error occurred: {error}")


def get_account_labels_gmail_api(request,service):
    """Fetch email counts by labels and return as a dictionary."""
    email_counts = {}
    try:
        labels_response = service.users().labels().list(userId='me').execute()
        labels = labels_response.get('labels', [])
        
        for label in labels:
            label_id = label['id']
            label_name = label['name']

            label_details = service.users().labels().get(userId='me', id=label_id).execute()
            message_count = label_details.get('messagesTotal', 0)

            email_counts[label_name] = message_count

        account_labels,created=GmailAccountLabelsCounts.objects.get_or_create(user=request.user)
        account_labels.label_info=email_counts
        account_labels.save()
    except HttpError as error:
        print(f"An error occurred: {error}")
        return {}



def get_gmail_data_at_intervals(service, start_time, end_time):
    start_timestamp = int(start_time.timestamp())
    end_timestamp = int(end_time.timestamp())

    # Query to filter emails in the time interval
    query = f"after:{start_timestamp} before:{end_timestamp}"
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])
    email_data = []

    if not messages:
        return {"message": f"No emails received between {start_time} and {end_time}", "emails": []}

    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        headers = msg['payload']['headers']
        subject = next((item['value'] for item in headers if item['name'] == 'Subject'), "No Subject")
        sender = next((item['value'] for item in headers if item['name'] == 'From'), "Unknown Sender")
        date = next((item['value'] for item in headers if item['name'] == 'Date'), "Unknown Date")
        snippet = msg.get('snippet', "No snippet available")

        email_data.append({
            "sender": sender,
            "subject": subject,
            "date": date,
            "snippet": snippet,
        })

    return {"message": "Emails fetched successfully.", "emails": email_data}
