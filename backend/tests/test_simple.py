import pytest
from fastapi.testclient import TestClient
from app.main import app

def test_health_check():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["message"] == "CRM MVP is running"

def test_invalid_endpoint():
    with TestClient(app) as client:
        response = client.get("/invalid-endpoint")
        assert response.status_code == 404
