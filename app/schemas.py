from pydantic import BaseModel
from typing import Optional

class CarCreate(BaseModel):
    manufacturer: str
    model: str
    year: int
    price: int
    fuel: Optional[str] = None
    transmission: str
    odometer: Optional[int] = None
    body_type: Optional[str] = None
    state: Optional[str] = None
    condition: Optional[str] = None

class CarUpdate(BaseModel):
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    price: Optional[int] = None
    fuel: Optional[str] = None
    transmission: Optional[str] = None
    odometer: Optional[int] = None
    body_type: Optional[str] = None
    state: Optional[str] = None
    condition: Optional[str] = None