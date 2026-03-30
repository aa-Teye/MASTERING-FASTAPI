import csv
import os
from datetime import datetime

# Create a folder specifically for our generated reports
EXPORT_DIR = "reports"

def generate_csv_report(vault_data: dict) -> str:
    """
    Takes the inventory dictionary, converts it to a CSV file,
    and returns the file path so FastAPI can send it to the user.
    """
    # Make sure the reports folder exists
    if not os.path.exists(EXPORT_DIR):
        os.makedirs(EXPORT_DIR)
        
    # Create a unique filename with today's date
    date_str = datetime.now().strftime("%Y-%m-%d")
    file_path = f"{EXPORT_DIR}/ONC_Inventory_{date_str}.csv"
    
    # Open the file and write the data
    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        # 1. Write the Header Row
        writer.writerow(["Item Name", "Quantity", "Status", "Assigned To"])
        
        # 2. Write the Data Rows
        for name, info in vault_data.items():
            writer.writerow([
                name, 
                info.get("qty", 0), 
                info.get("status", "Unknown"), 
                info.get("assigned_to", "Unassigned")
            ])
            
    return file_path