from googleapiclient.errors import HttpError
from gmail_manage.models import GmailAccountDetails,GmailAccountLabelsCounts
import base64
from email import message_from_bytes

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



def delete_emails_efficiently_by_labels(service, label, max_emails, order_by, no_of_days):
    """
    Delete emails by moving them to Trash, efficiently handling batches.
    :param service: Gmail API service instance.
    :param label: Gmail label to filter emails (e.g., 'IMPORTANT').
    :param max_emails: Maximum number of emails to delete. Use -1 for all.
    :param order_by: Order of emails ('newest' or 'oldest').
    """
    try:
        query = f"label:{label}"
        if order_by == "oldest":
            query += f" older_than:{no_of_days}d"  # Example for oldest 
        elif order_by == "newest":
            query += f" newer_than:{no_of_days}d"  # Example for newest

        total_deleted = 0
        next_page_token = None
        messages_log = []

        while True:
            response = service.users().messages().list(
                userId="me",
                q=query,
                maxResults=100,
                pageToken=next_page_token
            ).execute()

            messages = response.get("messages", [])
            if not messages:
                break

            for msg in messages:
                if max_emails != -1 and total_deleted >= max_emails:
                    messages_log.append(f"Reached the maximum limit of {max_emails} emails.")
                    return messages_log

                try:
                    service.users().messages().modify(
                        userId="me",
                        id=msg["id"],
                        body={"removeLabelIds": [], "addLabelIds": ["TRASH"]}
                    ).execute()
                    total_deleted += 1
                    messages_log.append(f"Deleted email with ID {msg['id']}.")
                except HttpError as error:
                    messages_log.append(f"Error deleting email with ID {msg['id']}: {error}")

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break

        messages_log.append(f"Successfully deleted {total_deleted} emails with label '{label}'.")
        return messages_log
    except HttpError as error:
        return [f"An error occurred: {error}"]



def fetch_emails_from_sender(service, sender_email):
    query = f"from:{sender_email}"
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])
    email_ids = [msg['id'] for msg in messages]
    return email_ids

def move_emails_to_trash(service, email_ids):
    for email_id in email_ids:
        try:
            service.users().messages().trash(userId='me', id=email_id).execute()
            print(f"Moved email with ID: {email_id} to Trash")
        except Exception as e:
            print(f"Failed to move email with ID: {email_id} to Trash. Error: {str(e)}")






# auto retrieval ----------------------------------------------------
# auto retrieval ----------------------------------------------------
def decode_email_content(raw_message):
    message_bytes = base64.urlsafe_b64decode(raw_message)
    message = message_from_bytes(message_bytes)
    return message

# Step 3: Get emails in a time interval with specific label
def fetch_emails_in_interval_automatic(service, start_time, end_time, label):
    # Convert datetime to UNIX timestamps
    start_timestamp = int(start_time.timestamp())
    end_timestamp = int(end_time.timestamp())
    
    # Query to filter emails in the time interval
    query = f"after:{start_timestamp} before:{end_timestamp}"
    results = service.users().messages().list(userId='me', q=query, labelIds=label).execute()
    messages = results.get('messages', [])

    if not messages:
        print(f"No emails received between {start_time} and {end_time} under label '{label}'")
        return
    
    print(f"Emails received between {start_time} and {end_time} under label '{label}':")
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id'], format='raw').execute()
        raw_message = msg['raw']
        decoded_message = decode_email_content(raw_message)

        # Extract headers
        headers = decoded_message.items()
        subject = decoded_message.get('Subject', "No Subject")
        sender = decoded_message.get('From', "Unknown Sender")
        date = decoded_message.get('Date', "Unknown Date")
        
        # Extract email body
        body = ""
        if decoded_message.is_multipart():
            for part in decoded_message.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = decoded_message.get_payload(decode=True).decode()
        
        print(f"Sender: {sender}")
        print(f"Subject: {subject}")
        print(f"Date: {date}")
        print(f"Body:\n{body}")