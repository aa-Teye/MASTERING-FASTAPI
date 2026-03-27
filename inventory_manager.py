# Project 04: ONC Media Inventory System
# Goal: Track Church Media Gear professionally

class InventoryManager:
    def __init__(self):
        # The 'Database' - Using a Dictionary for O(1) lookup speed
        self.vault = {
            "Sony NXCAM": {"qty": 2, "status": "Operational", "assigned_to": "Media Team"},
            "Blackmagic Switcher": {"qty": 1, "status": "Maintenance", "assigned_to": "Control Room"}
        }

    def add_item(self, name, qty, status="New", assigned="Unassigned"):
        """Adds a new piece of gear to the church vault."""
        self.vault[name] = {"qty": qty, "status": status, "assigned_to": assigned}
        print(f"✅ SUCCESS: {name} added to inventory.")

    def update_status(self, name, new_status):
        """Updates gear status (e.g., moving a mic to 'Repair')."""
        if name in self.vault:
            self.vault[name]["status"] = new_status
            print(f"🔄 STATUS CHANGE: {name} is now {new_status}.")
        else:
            print(f"❌ ERROR: '{name}' not found in the vault.")

    def search_by_status(self, status_type):
        """Returns a list of all gear with a specific status (e.g., 'Maintenance')."""
        results = {k: v for k, v in self.vault.items() if v['status'] == status_type}
        return results

# --- Test Execution (For your 8:30 AM block) ---
if __name__ == "__main__":
    onc_media = InventoryManager()
    
    # 1. Add a new item
    onc_media.add_item("Wireless Mic", 4, "Operational", "Youth Ministry")
    
    # 2. Update an item
    onc_media.update_status("Blackmagic Switcher", "Operational")
    
    # 3. View the whole vault
    print("\n--- Current ONC Vault ---")
    print(onc_media.vault)