from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os, tempfile, json

# ✅ Streamlit secrets import for cloud
try:
    from streamlit.runtime.secrets import secrets
except ImportError:
    secrets = None

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']


def gmail_login():
    """
    Authenticates user with Gmail using OAuth 2.0 credentials.
    - Uses Streamlit secrets on the cloud.
    - Uses local credentials.json when running locally.
    """
    creds = None

    # Use saved token if available
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If credentials are invalid or missing, perform login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # 🔐 On Streamlit Cloud, read from secrets instead of a file
            if secrets and "gcp" in secrets and "credentials_json" in secrets["gcp"]:
                creds_json = secrets["gcp"]["credentials_json"]
                with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as temp_file:
                    temp_file.write(creds_json.encode("utf-8"))
                    temp_file.flush()
                    flow = InstalledAppFlow.from_client_secrets_file(temp_file.name, SCOPES)
            else:
                # Local development fallback
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)

            creds = flow.run_local_server(port=0)

        # Save token locally (Streamlit ephemeral storage won't persist this)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Return Gmail service
    service = build('gmail', 'v1', credentials=creds)
    return service


def fetch_unread_emails(max_results=5):
    """
    Authenticate and fetch unread emails from Gmail inbox.
    Returns a list of dictionaries with subject, sender, and snippet.
    """
    service = gmail_login()
    results = service.users().messages().list(
        userId='me',
        labelIds=['INBOX'],
        q='is:unread',
        maxResults=max_results
    ).execute()

    messages = results.get('messages', [])
    emails = []

    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
        headers = msg_data['payload']['headers']
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(No Subject)')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), '(Unknown Sender)')
        snippet = msg_data.get('snippet', '')
        emails.append({'subject': subject, 'sender': sender, 'snippet': snippet})

    return emails
