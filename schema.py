from pydantic import BaseModel, Field
from typing import Optional

class GearBase(BaseModel):
    name: str = Field(..., min_length=2, example="Sony NXCAM")
    qty: int = Field(..., gt=0, description="Quantity must be greater than zero")
    status: str = Field(default="Operational", example="Maintenance")
    assigned_to: Optional[str] = "Media Team"

class GearCreate(GearBase):
    pass  # Used when creating new gear

class GearUpdate(BaseModel):
    status: Optional[str] = None
    assigned_to: Optional[str] = None