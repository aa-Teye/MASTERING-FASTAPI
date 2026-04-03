from datetime import datetime

def open_repair_ticket(gear_data: dict, issue: str, technician: str, cost: float) -> dict:
    """
    Creates a formal repair ticket and attaches it to the item's history.
    """
    # Create a unique Ticket ID using the current date and time
    ticket_id = f"REP-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # Check if the item already has a repair history list, if not, make one
    if "repair_history" not in gear_data:
        gear_data["repair_history"] = []
        
    ticket = {
        "ticket_id": ticket_id,
        "date_opened": datetime.now().strftime("%Y-%m-%d"),
        "issue": issue,
        "technician": technician,
        "estimated_cost": cost,
        "status": "In Progress"
    }
    
    # Add the ticket to the item's history
    gear_data["repair_history"].append(ticket)
    
    return ticket

def resolve_repair_ticket(gear_data: dict, ticket_id: str, final_cost: float) -> bool:
    """
    Finds an open ticket, marks it as resolved, and updates the final cost.
    """
    if "repair_history" not in gear_data:
        return False
        
    for ticket in gear_data["repair_history"]:
        if ticket["ticket_id"] == ticket_id and ticket["status"] == "In Progress":
            ticket["status"] = "Resolved"
            ticket["date_resolved"] = datetime.now().strftime("%Y-%m-%d")
            ticket["final_cost"] = final_cost
            return True
            
    return False