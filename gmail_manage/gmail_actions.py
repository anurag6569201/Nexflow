from googleapiclient.errors import HttpError
from gmail_manage.models import GmailAccountDetails

def get_account_details_gmail_api(request,service):
    """Fetch general details about the Gmail account."""
    try:
        profile = service.users().getProfile(userId='me').execute()
        account_details,created=GmailAccountDetails.objects.get_or_create(user=request.user)
        account_details.primary_email=profile.get('emailAddress')
        account_details.total_messages=profile.get('messagesTotal')
        account_details.total_threads=profile.get('threadsTotal')
        account_details.save()
        
        print("General Gmail Account Details:")
        print(f"Email Address: {profile.get('emailAddress')}")
        print(f"Total Messages: {profile.get('messagesTotal')}")
        print(f"Total Threads: {profile.get('threadsTotal')}")
        print(f"Last History ID: {profile.get('historyId')}")
    except HttpError as error:
        print(f"An error occurred: {error}")
