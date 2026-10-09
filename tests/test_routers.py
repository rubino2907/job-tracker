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


def test_get_applications_empty(db):
    response = client.get("/applications")
    assert response.status_code == 200
    assert response.json() == []

def test_get_applications(db):
    client.post(
        "/applications",
        json={
            "company": "Acme",
            "role": "Backend Developer",
            "status": "waiting",
            "applied_date": "2026-10-01",
        },
    )
    client.post(
        "/applications",
        json={
            "company": "Closer Consult",
            "role": "Backend Developer",
            "status": "waiting",
            "applied_date": "2026-10-02",
        },
    )

    response = client.get("/applications")

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[1]["company"] == "Closer Consult"

def test_get_application_not_found(db):
    missing_id = 99999
    response = client.get(f"/applications/{missing_id}")
    assert response.status_code == 404