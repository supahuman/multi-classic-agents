# agents/drive_agent.py

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from services.auth import Auth
import io

class DriveAgent:
    def __init__(self):
        self.service = build('drive', 'v3', credentials=Auth.authenticate_drive())

    def upload_to_drive(self, summary, title="Email Summary.txt"):
        """Upload summary to Google Drive."""
        try:
            # Create an in-memory buffer using io.BytesIO to simulate a file
            file_content = io.BytesIO(summary.encode('utf-8'))

            # Prepare the media for upload
            media = MediaIoBaseUpload(file_content, mimetype='text/plain')

            # Metadata for the uploaded file
            file_metadata = {
                'name': title,
                'mimeType': 'application/vnd.google-apps.document'
            }

            # Upload the file to Google Drive
            uploaded_file = self.service.files().create(
                body=file_metadata, media_body=media, fields='id'
            ).execute()

            return f"File uploaded successfully. File ID: {uploaded_file['id']}"
        except Exception as e:
            return f"Error uploading to Google Drive: {e}"
