import os
from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

# --- LOCAL MODULE IMPORTS ---
from inventory_manager import InventoryManager
from auth import verify_admin
from audit import get_recent_logs
from export import generate_csv_report
from upload_manager import save_gear_image

# Initialize the API
app = FastAPI(
    title="ONC Media Vault API",
    description="Professional Backend for Overcomers Nation Church Media Assets",
    version="1.0.0"
)


# Allow the future Next.js frontend to communicate with this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

# Make the images folder accessible to the web
os.makedirs("images", exist_ok=True)
app.mount("/images", StaticFiles(directory="images"), name="images")

# Initialize the Logic Engine
manager = InventoryManager()




@app.get("/inventory", tags=["Public"])
def get_all_gear():
    """Retrieve the full list of media assets."""
    return {"total_count": len(manager.vault), "assets": manager.vault}

@app.get("/inventory/search", tags=["Public"])
def search_gear(status: str = None):
    """Search for gear by status (e.g., ?status=Operational)."""
    if not status:
        raise HTTPException(status_code=400, detail="Please provide a status.")
    results = {name: info for name, info in manager.vault.items() if info["status"].lower() == status.lower()}
    return {"count": len(results), "results": results}

@app.get("/inventory/stats", tags=["Public"])
def get_inventory_stats():
    """Dashboard analytics for the media department."""
    total = len(manager.vault)
    operational = sum(1 for g in manager.vault.values() if g["status"].lower() == "operational")
    maintenance = sum(1 for g in manager.vault.values() if g["status"].lower() == "maintenance")
    health = (operational / total * 100) if total > 0 else 0

    return {
        "total_gear_count": total,
        "ready_to_use": operational,
        "needs_repair": maintenance,
        "department_health_score": f"{health:.1f}%"
    }



@app.post("/inventory/add", dependencies=[Depends(verify_admin)], tags=["Admin"])
def add_new_gear(gear: GearCreate):
    """Register a new piece of equipment."""
    if gear.name in manager.vault:
        raise HTTPException(status_code=400, detail="Item already exists.")
    manager.add_item(gear.name, gear.qty, gear.status, gear.assigned_to)
    return {"message": "Success", "added_item": gear}

@app.put("/inventory/update/{item_name}", dependencies=[Depends(verify_admin)], tags=["Admin"])
def update_gear_status(item_name: str, update_data: GearUpdate):
    """Update an item's status or assignment."""
    if item_name not in manager.vault:
        raise HTTPException(status_code=404, detail="Item not found.")
    manager.update_status(item_name, update_data.status)
    return {"message": f"Updated {item_name} status to {update_data.status}"}

@app.delete("/inventory/delete/{item_name}", dependencies=[Depends(verify_admin)], tags=["Admin"])
def delete_gear(item_name: str):
    """Permanently delete an item."""
    success = manager.delete_item(item_name)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found.")
    return {"message": f"🚨 Successfully deleted {item_name}."}

@app.get("/inventory/logs", dependencies=[Depends(verify_admin)], tags=["Admin"])
def view_system_logs(limit: int = 10):
    """View the most recent activity in the system."""
    logs = get_recent_logs(limit)
    return {"message": f"Showing last {limit} actions", "logs": logs}

@app.get("/inventory/export/csv", dependencies=[Depends(verify_admin)], tags=["Admin"])
def download_inventory_report():
    """Download a CSV spreadsheet of the current vault."""
    file_path =