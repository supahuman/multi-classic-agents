# agents/gmail_agent.py

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from services.auth import Auth
from tools.utils import extract_email_body
from tools.summarizer import summarize_email
from langchain_openai import ChatOpenAI

class GmailAgent:
    def __init__(self):
        self.service = build('gmail', 'v1', credentials=Auth.authenticate_gmail())

    def get_unread_emails(self):
        """Get unread emails from Gmail."""
        try:
            results = self.service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
            messages = results.get('messages', [])

            if not messages:
                return "No unread emails."

            email_summaries = []
            for msg in messages[:10]:  # Top 10 unread emails
                msg_data = self.service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
                payload = msg_data.get("payload", {})
                email_content = extract_email_body(payload)
                email_summaries.append(email_content)

            return email_summaries
        except HttpError as error:
            return f"An error occurred: {error}"

    def send_email(self, to, subject, body):
        """Send an email via Gmail."""
        try:
            sender = 'me'  # Replace with authenticated email
            message = self.create_message(sender, to, subject, body)
            send_message = self.service.users().messages().send(userId="me", body=message).execute()
            return f"Email sent to {to} with subject '{subject}'"
        except HttpError as error:
            return f"An error occurred: {error}"

    def create_message(self, sender, to, subject, body):
        """Create an email message."""
        message = MIMEMultipart()
        message['from'] = sender
        message['to'] = to
        message['subject'] = subject

        msg = MIMEText(body)
        message.attach(msg)

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        return {'raw': raw_message}
