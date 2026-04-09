import time
from datetime import datetime

def send_email_alert(to_email: str, subject: str, body: str):
    """
    Simu
    print(f"To:      {to_email}")
    print(f"Subject: {subject}")
    print("-" * 50)
    print(body)
    print("="*50 + "\n")
    
    # Also log it to our audit trail so we have a permanent record
    from audit import log_action
    log_action("NOTIFICATION", "System Alert", f"Email sent to {to_email} regarding: {subject}")