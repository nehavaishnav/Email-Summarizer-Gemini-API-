import os.path
import base64
import re
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Define Gmail API scope
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_email_service():
    """Authenticate and return Gmail API service."""
    creds = None
    token_path = 'credentials/token.json'
    credentials_path = 'credentials/credentials.json'

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

def clean_html(raw_html):
    clean_text = re.sub('<.*?>', '', raw_html)
    return clean_text

def get_emails(max_results=5):
    """Fetch emails and return list of dicts with subject, from, and body."""
    service = get_email_service()
    results = service.users().messages().list(userId='me', maxResults=max_results).execute()
    messages = results.get('messages', [])

    emails = []

    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        payload = msg_data.get('payload', {})
        headers = payload.get('headers', [])

        subject = ''
        sender = ''
        for header in headers:
            if header['name'] == 'Subject':
                subject = header['value']
            elif header['name'] == 'From':
                sender = header['value']

        # Get email body
        parts = payload.get('parts', [])
        body = ''
        if parts:
            for part in parts:
                if part['mimeType'] == 'text/plain':
                    data = part['body'].get('data')
                    if data:
                        body = base64.urlsafe_b64decode(data).decode()
                        break
                elif part['mimeType'] == 'text/html':
                    data = part['body'].get('data')
                    if data:
                        body = base64.urlsafe_b64decode(data).decode()
                        body = clean_html(body)
                        break
        else:
            data = payload.get('body', {}).get('data')
            if data:
                body = base64.urlsafe_b64decode(data).decode()

        emails.append({
            'subject': subject,
            'from': sender,
            'body': body
        })

    return emails
