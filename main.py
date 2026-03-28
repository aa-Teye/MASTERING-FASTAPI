from fastapi import FastAPI, HTTPException
from inventory_manager import InventoryManager # Importing your logic!

# 1. Initialize the API and your Logic Engine
app = FastAPI(title="ONC Media Inventory API")
manager = InventoryManager()

# 2. READ: Get all gear (The "Dashboard" view)
@app.get("/inventory")
def get_all_inventory():
    return manager.vault

# 3. READ: Get a specific item
@app.get("/inventory/{item_name}")
def get_item(item_name: str):
    item = manager.vault.get(item_name)
    if not item:
        raise HTTPException(status_code=404, detail="Gear not found")
    return item

# 4. CREATE: Add new gear via the web
@app.post("/inventory/add")
def add_new_gear(name: str, qty: int, status: str = "Operational"):
    manager.add_item(name, qty, status)
    return {"message": f"Successfully added {name}", "data": manager.vault[name]}