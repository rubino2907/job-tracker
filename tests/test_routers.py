from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_create_application(db):
    company = "Acme"
    role = "Consultor Junior"
    status = "waiting"
    applied_date = "2025-12-10"
    response = client.post(
        "/applications",
        json={
            "company": company,
            "role": role,
            "status": status,
            "applied_date": applied_date,
        },
    )
    assert response.status_code == 200
    assert response.json()["company"] == company
    assert response.json()["role"] == role
    assert response.json()["status"] == status
