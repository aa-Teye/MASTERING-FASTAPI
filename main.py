from fastapi import FastAPI, HTTPException, Depends
from inventory_manager import InventoryManager
from schemas import GearCreate, GearUpdate
from auth import verify_admin  # Importing your new security bouncer!

app = FastAPI(title="ONC Media Vault API")
manager = InventoryManager()

# --- PUBLIC ROUTES (Anyone can view) ---

@app.get("/inventory")
def get_all_gear():
    return manager.vault

@app.get("/inventory/search")
def search_gear(status: str = None):
    if not status:
        raise HTTPException(status_code=400, detail="Please provide a status.")
    results = {name: info for name, info in manager.vault.items() if info["status"].lower() == status.lower()}
    return {"count": len(results), "results": results}


# --- SECURE ADMIN ROUTES (Requires Password) ---

# Notice the 'dependencies=[Depends(verify_admin)]' added here!
@app.post("/inventory/add", dependencies=[Depends(verify_admin)])
def add_new_gear(gear: GearCreate):
    if gear.name in manager.vault:
        raise HTTPException(status_code=400, detail="Item already exists.")
    manager.add_item(gear.name, gear.qty, gear.status, gear.assigned_to)
    return {"message": "Success", "added_item": gear}

@app.delete("/inventory/delete/{item_name}", dependencies=[Depends(verify_admin)])
def delete_gear(item_name: str):
    if item_name not in manager.vault:
        raise HTTPException(status_code=404, detail="Item not found.")
    del manager.vault[item_name]
    return {"message": f"🚨 Successfully deleted {item_name}."}