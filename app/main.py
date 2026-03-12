from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, text
from app.schemas import CarCreate
from app.auth import require_api_key
from pathlib import Path

app = FastAPI(title = "Car Recommendation API")

BASE_DIR = Path(__file__).resolve().parent.parent
engine = create_engine(f"sqlite:///{BASE_DIR /'cars.db'}")


@app.get("/")
def root():
    return {"message": "Car Recommendation API is running"}

@app.get("/cars")
def get_cars(limit: int = 10):
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
    return {"message": "Admin access granted"}

@app.post("/cars", status_code=201)
def create_car(car: CarCreate, api_key: str = Depends(require_api_key)):
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                 INSERT INTO cars (manufacturer, model, year, price, fuel, transmission, odometer, body_type, state, condition)
                 VALUES (:manufacturer, :model, :year, :price, :fuel, :transmission, :odometer, :body_type, :state, :condition)
                 """),
                 {
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
        return {"message": "Car created successfully", "listing_id": result.lastrowid}