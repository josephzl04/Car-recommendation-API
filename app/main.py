from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy import create_engine, text
from app.schemas import CarCreate, CarUpdate
from app.auth import require_api_key
from pathlib import Path
from fastapi_mcp import FastApiMCP
import uuid
from typing import Optional

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
    with engine.begin() as conn:
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
    return {"message": "Car created successfully", "listing_id": new_listing_id}

@app.put("/cars/{listing_id}")
def update_car(listing_id: int, car: CarUpdate, api_key: str = Depends(require_api_key)):
    """
    Update an existing car listing in the database.
    Requires a valid API key in the X-API-Key header.
    Only accessible to admins
    """
    with engine.begin() as conn:
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

    return {"message": "Car updated successfully", "listing_id": listing_id}

@app.delete("/cars/{listing_id}", status_code=200)
def delete_car(listing_id: int, api_key: str = Depends(require_api_key)):
    """
    Delete a car from db using listing ID.
    Requires a valid API key in the X-API-Key header.
    Only accessible by admins.
    """
    with engine.begin() as conn:
        result = conn.execute(
            text("SELECT * FROM cars WHERE listing_id = :listing_id"),
            {"listing_id": listing_id}
        )
        existing_car = result.fetchone()
        if not existing_car:
            raise HTTPException(status_code=404, detail="Car not found")

        conn.execute(
            text("DELETE FROM cars WHERE listing_id = :listing_id"),
            {"listing_id": listing_id}
        )
    return {"message": "Car successfully deleted", "listing_id": listing_id}


@app.get("/cars/search")
def search_cars(
    manufacturer: Optional[str] = Query(None, description="Filter by manufacturer e.g. toyota"),
    min_price: Optional[int] = Query(None, description="Minimum price in USD"),
    max_price: Optional[int] = Query(None, description="Maximum price in USD"),
    min_year: Optional[int] = Query(None, description="Minimum year e.g. 2015"),
    max_year: Optional[int] = Query(None, description="Maximum year e.g. 2022"),
    fuel: Optional[str] = Query(None, description="Fuel type e.g. gas, diesel, electric"),
    transmission: Optional[str] = Query(None, description="Transmission type e.g. automatic, manual"),
    state: Optional[str] = Query(None, description="US state abbreviation e.g. ca, tx"),
    max_odometer: Optional[int] = Query(None, description="Maximum mileage"),
    condition: Optional[str] = Query(None, description="Condition e.g. good, excellent, fair"),
    limit: int = Query(20, ge=1, le=100, description="Number of results to return")):
    """
    Searching for cars with filters
    """

    filters = []
    params = {"limit": limit}

    if manufacturer:
        filters.append("LOWER(manufacturer) = LOWER(:manufacturer)")
        params["manufacturer"] = manufacturer
    if min_price:
        filters.append("price >= :min_price")
        params["min_price"] = min_price
    if max_price:
        filters.append("price <= :max_price")
        params["max_price"] = max_price
    if min_year:
        filters.append("year >= :min_year")
        params["min_year"] = min_year
    if max_year:
        filters.append("year <= :max_year")
        params["max_year"] = max_year
    if fuel:
        filters.append("LOWER(fuel) = LOWER(:fuel)")
        params["fuel"] = fuel
    if transmission:
        filters.append("LOWER(transmission) = LOWER(:transmission)")
        params["transmission"] = transmission
    if state:
        filters.append("LOWER(state) = LOWER(:state)")
        params["state"] = state
    if max_odometer:
        filters.append("odometer <= :max_odometer")
        params["max_odometer"] = max_odometer
    if condition:
        filters.append("LOWER(condition) = LOWER(:condition)")
        params["condition"] = condition

    where_clause = "WHERE " + " AND ".join(filters) if filters else ""

    with engine.connect() as conn:
        rows = conn.execute(text(f"""
            SELECT listing_id, manufacturer, model, year, price, fuel, transmission, odometer, body_type, state, condition
            FROM cars {where_clause} ORDER BY price ASC LIMIT :limit """), params).fetchall()

    if not rows:
        raise HTTPException(status_code=404, detail="No cars found matching your filters")
    
    return {"count": len(rows), "cars": [dict(r._mapping) for r in rows]}

@app.get("/cars/recommend")
def recommend_cars(
    budget: int = Query(..., gt=0, description="Maximum budget in USD"),
    max_odometer: int = Query(100000, gt=0, description="Maximum mileage"),
    min_year: int = Query(2010, description="Minimum model year"),
    fuel: Optional[str] = Query(None, description="Preferred fuel type e.g. gas, diesel, electric"),
    transmission: Optional[str] = Query(None, description="Preferred transmission e.g. automatic, manual"),
    limit: int = Query(10, ge=1, le=50, description="Number of recommendations"),):
    """
    Recommends best value cars based on weight scoring
    Higher score = higher ranked in recommended list
    Scoring:
    - Price: 35%
    - Mileage: 25%
    - Year recency: 20%
    - Fuel match: 10%
    - Transmission match: 10%
    """

    filters = ["price <= :budget", "odometer <= :max_odometer", "price >= :min_price", "year >= :min_year"]
    params = {
        "budget": budget,
        "max_odometer": max_odometer,
        "min_price": budget * 0.1, # filters out bad / useless data
        "min_year": min_year,
        "limit": limit,
        "fuel": fuel,
        "transmission": transmission}

    where_clause = "WHERE " + " AND ".join(filters)

    with engine.connect() as conn:
        rows = conn.execute(text(f"""
            SELECT listing_id, manufacturer, model, year, price, fuel,
                   transmission, odometer, body_type, state, condition,
                   ROUND(
                    (1.0 - CAST(price AS REAL) / :budget) * 0.35
                    + (1.0 - CAST(odometer AS REAL) / :max_odometer) * 0.25
                    + ((CAST(year AS REAL) - :min_year) / (2026 - :min_year)) * 0.20
                    + CASE WHEN :fuel IS NOT NULL AND LOWER(fuel) = LOWER(:fuel) THEN 0.10 ELSE 0 END
                    + CASE WHEN :transmission IS NOT NULL AND LOWER(transmission) = LOWER(:transmission) THEN 0.10 ELSE 0 END
                , 3) AS value_score
                                 
            FROM cars
            {where_clause}
            ORDER BY value_score DESC
            LIMIT :limit
        """), params).fetchall()

    if not rows:
        raise HTTPException(status_code=404, detail="No cars found matching your requirements")

    return {
        "budget": budget,
        "max_odometer": max_odometer,
        "min_year": min_year,
        "count": len(rows),
        "recommendations": [dict(r._mapping) for r in rows]
    }


@app.get("/cars/{listing_id}")
def get_car(listing_id: int):
    """Get a single car by ID"""
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM cars WHERE listing_id = :id"),
            {"id": listing_id}
        ).fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Car not found")
    return dict(result._mapping)