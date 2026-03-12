from pydantic import BaseModel
from typing import List, Optional

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