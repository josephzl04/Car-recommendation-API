from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy import create_engine, text
from app.schemas import CarCreate, CarUpdate
from app.auth import require_api_key
from pathlib import Path
from fastapi_mcp import FastApiMCP
import uuid

app = FastAPI(title = "Car Recommendation API")

BASE_DIR = Path(__file__).resolve().parent.parent
engine = create_engine(f"sqlite:///{BASE_DIR /'cars.db'}")

mcp = FastApiMCP(app)
mcp.mount_http()

@app.get("/")
def root():
    """Check the API is running."""
    return {"message": "Car Recommendation API is running"}

@app.get("/cars")
def get_cars(limit: int = Query(10, ge=1, le=100)):
    """
    Retrieve a list of cars from the database.
    Use the limit parameter to control how many cars are returned (default is 10).
    """
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                 SELECT listing_id, manufacturer, model, year, price, fuel, transmission, odometer, body_type, state
                 FROM cars
                 LIMIT :limit
                 """),
                 {"limit": limit}
        )

        cars = []
        for row in result:
            cars.append({
                "listing_id": row[0],
                "manufacturer": row[1],
                "model": row[2],
                "year": row[3],
                "price": row[4],
                "fuel": row[5],
                "transmission": row[6],
                "odometer": row[7],
                "body_type": row[8],
                "state": row[9],
            })
        return {"count": len(cars), "cars": cars}
    
@app.get("/admin/test")
def admin_test(api_key: str = Depends(require_api_key)):
    """Protected endpoint to verify API key is working correctly"""
    return {"message": "Admin access granted"}

@app.post("/cars", status_code=201)
def create_car(car: CarCreate, api_key: str = Depends(require_api_key)):
    """
    Add a new car listing to the database. 
    Requires a valid API key in the X-API-Key header.
    Only accessible to admins
    """
    new_listing_id = int(uuid.uuid4().int % 1_000_000_000)  # Generate a unique listing_id
    with engine.connect() as conn:
        conn.execute(
            text("""
                INSERT INTO cars (listing_id, manufacturer, model, year, price, fuel,
                                  transmission, odometer, body_type, state, condition)
                VALUES (:listing_id, :manufacturer, :model, :year, :price, :fuel,
                        :transmission, :odometer, :body_type, :state, :condition)
            """),
           {
                "listing_id": new_listing_id,
                "manufacturer": car.manufacturer,
                "model": car.model,
                "year": car.year,
                "price": car.price,
                "fuel": car.fuel,
                "transmission": car.transmission,
                "odometer": car.odometer,
                "body_type": car.body_type,
                "state": car.state,
                "condition": car.condition
            }
        )
        conn.commit()
    return {"message": "Car created successfully", "listing_id": new_listing_id}

@app.put("/cars/{listing_id}")
def update_car(listing_id: int, car: CarUpdate, api_key: str = Depends(require_api_key)):
    """
    Update an existing car listing in the database.
    Requires a valid API key in the X-API-Key header.
    Only accessible to admins
    """
    with engine.connect() as conn:
        # Check if the car exists
        result = conn.execute(
            text("SELECT * FROM cars WHERE listing_id = :listing_id"),
            {"listing_id": listing_id}
        )
        existing_car = result.fetchone()
        if not existing_car:
            raise HTTPException(status_code=404, detail="Car not found")

        # Makes update dynamic instead of forcing all fields to be sent
        update_fields = []
        update_values = {"listing_id": listing_id}
        for field in car.model_dump(exclude_unset=True):
            update_fields.append(f"{field} = :{field}")
            update_values[field] = getattr(car, field)

        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields provided for update")

        update_query = f"UPDATE cars SET {', '.join(update_fields)} WHERE listing_id = :listing_id"
        conn.execute(text(update_query), update_values)
        conn.commit()

    return {"message": "Car updated successfully", "listing_id": listing_id}