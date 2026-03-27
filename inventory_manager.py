# Project 04: ONC Media Inventory Logic
class ONCInventory:
    def __init__(self):
        # Initial Data (Dictionary of Dictionaries)
        self.gear = {
            "Sony NXCAM": {"qty": 2, "status": "Good"},
            "vMix PC": {"qty": 1, "status": "Running"}
        }

    def add_item(self, name, qty, status):
        self.gear[name] = {"qty": qty, "status": status}
        return f"✅ Added {name}"

    def get_status(self, name):
        if name in self.gear:
            item = self.gear[name]
            return f"Inventory Check: {name} | Qty: {item['qty']} | Status: {item['status']}"
        return " Item not found."

    def list_all(self):
        return self.gear

# --- Test your code here ---
onc = ONCInventory()
print(onc.add_item("Wireless Mic", 4, "Maintenance"))
print(onc.get_status("Sony NXCAM"))
