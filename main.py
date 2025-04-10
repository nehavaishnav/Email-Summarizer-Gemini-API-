# dumy/main.py

from gmail_reader import get_emails
from summarizer import summarize_email

print("📥 Fetching Emails...\n")
emails = get_emails(max_results=5)

for email in emails:
    print(f"Subject: {email['subject']}")
    print(f"From: {email['from']}")
    print("Summary:")
    print(summarize_email(email["body"]))
    print("=" * 50 + "\n")
