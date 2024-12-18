from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os

# Scopes for Gmail API (modify is sufficient)
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def authenticate_gmail_for_modify():
    """Authenticate and create a Gmail API client."""
    creds = None
    token_path = os.path.join(os.path.dirname(__file__), 'tokens/modify_token.json')
    credentials_path = os.path.join(os.path.dirname(__file__), 'credentials/credentials.json')

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            credentials_path, SCOPES
        )
        creds = flow.run_local_server(port=0)
        with open(token_path, "w") as token:
            token.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)