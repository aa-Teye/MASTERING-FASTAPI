from fastapi import FastAPI, HTTPException, status
from typing import Dict
from inventory_manager import InventoryManager
from schemas import GearCreate, GearUpdate

app = FastAPI(
    title="ONC Media Inventory System",
    description="Professional Backend for Overcomers Nation Church Media Assets",
    version="1.0.0"
)

# Initialize our logic engine
manager = InventoryManager()

@app.get("/inventory", tags=["Inventory"])
def list_all_gear():
    """Retrieve the full list of media assets in the vault."""
    return {"total_count": len(manager.vault), "assets": manager.vault}

@app.post("/inventory", status_code=status.HTTP_201_CREATED, tags=["Inventory"])
def add_gear(gear: GearCreate):
    """Register a new piece of equipment with validation."""
    if gear.name in manager.vault:
        raise HTTPException(status_code=400, detail="Item already exists")
    
    manager.add_item(gear.name, gear.qty, gear.status, gear.assigned_to)
    return {"message": "Asset registered successfully", "asset": gear}

@app.patch("/inventory/{name}", tags=["Inventory"])
def update_gear(name: str, update_data: GearUpdate):
    """Partially update an asset's status or assignment."""
    if name not in manager.vault:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    if update_data.status:
        manager.update_status(name, update_data.status)
    
    return {"message": f"Updated {name}", "current_data": manager.vault[name]}