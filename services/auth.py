# services/auth.py

import pickle
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Define token paths
GMAIL_TOKEN_PATH = "token_gmail.pickle"
GDRIVE_TOKEN_PATH = "token_drive.pickle"

# Define SCOPES
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send']
GDRIVE_SCOPES = ['https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive']

class Auth:
    @staticmethod
    def authenticate_gmail():
        """Authenticate and return Gmail service."""
        creds = None
        if os.path.exists(GMAIL_TOKEN_PATH):
            with open(GMAIL_TOKEN_PATH, 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=8080)

            with open(GMAIL_TOKEN_PATH, 'wb') as token:
                pickle.dump(creds, token)

        return creds

    @staticmethod
    def authenticate_drive():
        """Authenticate and return Google Drive service."""
        creds = None
        if os.path.exists(GDRIVE_TOKEN_PATH):
            with open(GDRIVE_TOKEN_PATH, 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', GDRIVE_SCOPES)
                creds = flow.run_local_server(port=8081)

            with open(GDRIVE_TOKEN_PATH, 'wb') as token:
                pickle.dump(creds, token)

        return creds
