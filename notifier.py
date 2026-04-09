import time
from datetime import datetime

def send_email_alert(to_email: str, subject: str, body: str):
    """
    Simulates sending an email via a background worker.
    In production, this would connect to SendGrid or Gmail SMTP.
    """
    # Simulate network delay of connecting to an email server
    time.sleep(2) 
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Format a beautiful terminal output to prove the "email" sent
    print("\n" + "="*50)
    print(f"📧 NEW EMAIL DISPATCHED [{timestamp}]")
    print(f"To:      {to_email}")
    print(f"Subject: {subject}")
    print("-" * 50)
    print(body)
    print("="*50 + "\n")
    
    # Also log it to our audit trail so we have a permanent record
    from audit import log_action
    log_action("NOTIFICATION", "System Alert", f"Email sent to {to_email} regarding: {subject}")