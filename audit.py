import datetime
import os

LOG_FILE = "system_logs.txt"

def log_action(action_type: str, item_name: str, details: str = ""):
    """
    Appends a timestamped record of what happened to the log file.
    Example: [2026-03-30 10:15:00] UPDATE | Sony NXCAM | Changed status to Maintenance
    """
    # Get the exact current date and time
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Format the log message
    log_entry = f"[{timestamp}] {action_type.upper()} | Item: {item_name} | {details}\n"
    
    # Open the file in "a" (append) mode so it adds to the bottom without deleting old logs
    with open(LOG_FILE, "a") as file:
        file.write(log_entry)

def get_recent_logs(limit: int = 10):
    """Reads the log file and returns the most recent activities."""
    if not os.path.exists(LOG_FILE):
        return ["No logs found."]
    
    with open(LOG_FILE, "r") as file:
        lines = fi
