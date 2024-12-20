import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail_for_readonly():
    """Authenticate and create a Gmail API client."""
    token_path = os.path.join(os.path.dirname(__file__), 'tokens/token.json')
    credentials_path = os.path.join(os.path.dirname(__file__), 'credentials/credentials.json')
    creds = None

    # Load existing credentials
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # Refresh token if expired
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    elif not creds or not creds.valid:
        # Authenticate if no valid credentials
        flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
        creds = flow.run_local_server(port=0)
        # Save the credentials for future use
        with open(token_path, "w") as token:
            token.write(creds.to_json())

    # Return the Gmail API client
    return build("gmail", "v1", credentials=creds)
