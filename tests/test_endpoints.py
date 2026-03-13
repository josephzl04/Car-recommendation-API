import pytest
from sqlalchemy import create_engine, text
from fastapi.testclient import TestClient
from app.main import app
import app.main as main_module
from dotenv import load_dotenv
import os

load_dotenv()

client = TestClient(app)
api_key = os.getenv("API_KEY")
headers = {"X-API-Key": api_key}

@pytest.fixture(autouse=True)
def use_test_db():
    test_engine = create_engine("sqlite:///test.db", connect_args={"check_same_thread": False})

    # create temporary test database
    with test_engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS cars (
                listing_id INTEGER PRIMARY KEY,
                manufacturer TEXT,
                model TEXT,
                year INTEGER,
                price INTEGER,
                fuel TEXT,
                transmission TEXT,
                odometer INTEGER,
                body_type TEXT,
                state TEXT,
                condition TEXT
            )
        """))
        conn.commit()
    main_module.engine = test_engine
    yield
    with test_engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS cars"))
        conn.commit()
    test_engine.dispose()
    if os.path.exists("test.db"):
        os.remove("test.db")

# creates a car with valid data and api key, checks it was created and assigned an ID
def test_create_car():
    response = client.post("/cars", json={
        "manufacturer": "toyota",
        "model": "camry",
        "year": 2018,
        "price": 15000,
        "fuel": "gas",
        "transmission": "automatic",
        "odometer": 45000,
        "state": "ca",
        "condition": "good"
    }, headers=headers)
    assert response.status_code == 201
    assert "listing_id" in response.json()

def test_update_car():
    create_response = client.post("/cars", json={
        "manufacturer": "honda",
        "model": "civic",
        "year": 2017,
        "price": 12000,
        "fuel": "gas",
        "transmission": "manual",
        "odometer": 60000,
        "condition": "fair"
    }, headers=headers)
    listing_id = create_response.json()["listing_id"]

    # update the car
    update_response = client.put(f"/cars/{listing_id}", json={
        "price": 11000,
        "odometer": 55000,
        "condition": "good"
    }, headers=headers)
    assert update_response.status_code == 200
    assert update_response.json()["listing_id"] == listing_id

    # verify data was updated in db
    with main_module.engine.connect() as conn:
        result = conn.execute(text("SELECT price, odometer, condition FROM cars WHERE listing_id = :id"), {"id": listing_id})
        row = result.fetchone()
        assert row[0] == 11000
        assert row[1] == 55000
        assert row[2] == "good"

def test_update_car_not_found():
    response = client.put("/cars/999999999", json={"price": 5000}, headers=headers)
    assert response.status_code == 404

def test_delete_car():
    create_response = client.post("/cars", json={
        "manufacturer": "ford",
        "model": "mustang",
        "year": 2020,
        "price": 25000,
        "fuel": "gas",
        "transmission": "automatic",
        "odometer": 20000
    }, headers=headers)

    listing_id = create_response.json()["listing_id"]

    delete_response = client.delete(f"/cars/{listing_id}", headers=headers)
    assert delete_response.status_code == 200
    assert delete_response.json()["listing_id"] == listing_id

    with main_module.engine.connect() as conn:
        row = conn.execute(
            text("SELECT listing_id FROM cars WHERE listing_id = :id"),
            {"id": listing_id}
        ).fetchone()
        assert row is None

def test_delete_car_not_found():
    response = client.delete("/cars/999999999",headers=headers)
    assert response.status_code == 404

# test endpoint is working
def test_get_cars():
    response = client.get("/cars")
    assert response.status_code == 200
    assert "cars" in response.json()
    assert "count" in response.json()

def test_get_car_by_id():
    create_response = client.post("/cars", json={
        "manufacturer": "nissan",
        "model": "altima",
        "year": 2019,
        "price": 14000,
        "fuel": "gas",
        "transmission": "automatic",
        "odometer": 30000
    }, headers=headers)
    listing_id = create_response.json()["listing_id"]

    get_response = client.get(f"/cars/{listing_id}")
    assert get_response.status_code == 200
    assert get_response.json()["listing_id"] == listing_id
    assert get_response.json()["manufacturer"] == "nissan"

# search for a car id that doesnt exist
def test_get_car_by_id_not_found():
    response = client.get("/cars/999999999")
    assert response.status_code == 404

# create a car then search for it using the endpoint, verifies correct result
def test_search_cars():
    client.post("/cars", json={
        "manufacturer": "subaru",
        "model": "outback",
        "year": 2018,
        "price": 18000,
        "fuel": "gas",
        "transmission": "automatic",
        "odometer": 40000,
        "state": "tx"
    }, headers=headers)

    response = client.get("/cars/search?manufacturer=subaru&state=tx")
    assert response.status_code == 200
    assert response.json()["count"] >= 1
    assert response.json()["cars"][0]["manufacturer"] == "subaru"

# search for a random manufacturer that doesnt exist
def test_search_cars_no_results():
    response = client.get("/cars/search?manufacturer=nonexistent")
    assert response.status_code == 404

# create and add 3 cars to db, requests limit of 2, verifies that no  more than 2 cars are returned
def test_get_cars_limit():
    for i in range(3):
        client.post("/cars", json={
            "manufacturer": "toyota",
            "model": "camry",
            "year": 2018,
            "price": 15000,
            "fuel": "gas",
            "transmission": "automatic",
            "odometer": 45000
        }, headers=headers)

    response = client.get("/cars?limit=2")
    assert response.status_code == 200
    assert response.json()["count"] <= 2

# creates a car and then tests the recommendation endpoint to ensure it returns at least 1 recommendation based on the created car
def test_recommend_cars():
    client.post("/cars", json={
        "manufacturer": "mazda",
        "model": "cx-5",
        "year": 2019,
        "price": 20000,
        "fuel": "gas",
        "transmission": "automatic",
        "odometer": 25000,
        "state": "fl",
        "condition": "good"
    }, headers=headers)
    response = client.get("/cars/recommend?budget=25000&min_year=2015")
    assert response.status_code == 200
    assert "recommendations" in response.json()
    assert response.json()["count"] >= 1

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Car Recommendation API is running"}

