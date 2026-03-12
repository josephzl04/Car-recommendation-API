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

def test_create_car_without_auth():
    response = client.post("/cars", json={
        "manufacturer": "toyota",
        "model": "camry",
        "year": 2018,
        "price": 15000,
        "fuel": "gas",
        "transmission": "automatic",
        "odometer": 45000
    })
    assert response.status_code == 401


def test_update_car():
    # first create a car to update
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

def test_update_car_without_auth():
    response = client.put("/cars/123", json={"price": 5000})
    assert response.status_code == 401


def test_delete_car():
    # create a car to delete
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

def test_delete_car_without_auth():
    response = client.delete("/cars/123")
    assert response.status_code == 401