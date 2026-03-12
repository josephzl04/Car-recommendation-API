from fastapi.testclient import TestClient
from app.main import app
from dotenv import load_dotenv
import os

# ensures .env variables are loaded for testing
load_dotenv()

client = TestClient(app)

# send request without API key (as user instead of admin)
def test_admin_requires_key():
    response = client.get("/admin/test")
    assert response.status_code == 401
def test_admin_with_valid_key():
    api_key = os.getenv("API_KEY")
    response = client.get("/admin/test", headers={"X-API-Key": api_key})
    assert response.status_code == 200
def test_admin_with_invalid_key():
    response = client.get("/admin/test", headers={"X-API-Key": "invalid"})
    assert response.status_code == 401
    