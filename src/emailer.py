from googleapiclient.discovery import build
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64

def send_email(to_email, subject, body, creds):
    service = build('gmail', 'v1', credentials=creds)
    message = MIMEMultipart()
    message['to'] = to_email
    message['subject'] = subject
    message.attach(MIMEText(body, 'plain'))
    
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    service.users().messages().send(userId='me', body={'raw': raw}).execute()