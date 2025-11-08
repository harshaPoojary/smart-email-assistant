from reply_utils import generate_reply
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os

# Gmail API Scopes (read, send, modify)
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']


def gmail_login():
    """
    Authenticate user via OAuth and return Gmail service object.
    Creates a 'token.json' file to store credentials for reuse.
    """
    creds = None

    # Use saved token if available
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If credentials are invalid or missing, perform login flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save credentials for future runs
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Create Gmail service
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
        msg_data = service.users().messages().get(
            userId='me',
            id=msg['id']
        ).execute()

        headers = msg_data['payload']['headers']
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(No Subject)')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), '(Unknown Sender)')
        snippet = msg_data.get('snippet', '')

        emails.append({
            'subject': subject,
            'sender': sender,
            'snippet': snippet
        })

    return emails


# 🧠 Main block: runs only when executing this script directly, not when imported
if __name__ == "__main__":
    from llm_utils import summarize_emails_extractive as summarize_emails

    print("✅ Gmail login successful!\n")
    print("Fetching unread emails...\n")
    unread_emails = fetch_unread_emails()

    if unread_emails:
        for idx, email in enumerate(unread_emails[:5], start=1):
            print(f"--- Email {idx} ---")
            print(f"From: {email['sender']}")
            print(f"Subject: {email['subject']}")
            print(f"Snippet: {email['snippet']}\n")

        print("🧠 Generating summary...\n")
        summary = summarize_emails(unread_emails)
        print(summary)

        print("\n💌 Generating sample reply drafts...\n")
        for email in unread_emails[:3]:
            reply = generate_reply(email)
            print(f"Reply suggestion for: {email['subject']}")
            print(reply)
            print("-" * 80)
    else:
        print("📭 No unread emails found.")
