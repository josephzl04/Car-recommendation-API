from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

app = FastAPI(title = "Car Recommendation API")

engine = create_engine("sqlite:///cars.db")

#authentication
load_dotenv()
API_KEY = os.getenv("API_KEY")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def require_api_key(api_key: str = Depends(api_key_header)):
    if api_key == API_KEY:
        return api_key
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )

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
