from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def make_application(company="Acme"):
    return {
        "company": company,
        "role": "Backend Developer",
        "status": "waiting",
        "applied_date": "2026-10-01",
    }


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


def test_create_application_invalid_status(db):
    body = make_application()
    body["status"] = "fail"

    response = client.post("/applications", json=body)

    assert response.status_code == 422


def test_create_application_invalid_date(db):
    body = make_application()
    body["applied_date"] = "10/12/2025"

    response = client.post("/applications", json=body)

    assert response.status_code == 422


def test_get_applications_empty(db):
    response = client.get("/applications")
    assert response.status_code == 200
    assert response.json() == []


def test_get_applications(db):
    client.post("/applications", json=make_application())
    client.post("/applications", json=make_application("Closer Consult"))

    response = client.get("/applications")

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[1]["company"] == "Closer Consult"


def test_get_application(db):
    first = client.post("/applications", json=make_application())
    second = client.post("/applications", json=make_application("Closer Consult"))

    application_id = second.json()["id"]
    response = client.get(f"/applications/{application_id}")

    assert response.status_code == 200
    assert response.json()["company"] == "Closer Consult"


def test_get_application_not_found(db):
    missing_id = 99999
    response = client.get(f"/applications/{missing_id}")
    assert response.status_code == 404


def test_patch_application(db):
    created = client.post("/applications", json=make_application())
    application_id = created.json()["id"]
    response = client.patch(
        f"/applications/{application_id}", json={"status": "interview_scheduled"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "interview_scheduled"


def test_patch_application_invalid_status(db):
    created = client.post("/applications", json=make_application())
    application_id = created.json()["id"]
    response = client.patch(f"/applications/{application_id}", json={"status": "fail"})
    assert response.status_code == 422


def test_patch_application_not_found(db):
    missing_id = 99999
    response = client.patch(f"/applications/{missing_id}", json={"status": "waiting"})
    assert response.status_code == 404


def test_delete_application(db):
    created = client.post("/applications", json=make_application())
    application_id = created.json()["id"]
    response = client.delete(f"/applications/{application_id}")
    assert response.status_code == 200
    response = client.get(
        f"/applications/{application_id}"
    )  # novo pedido: a candidatura ainda existe?
    assert response.status_code == 404


def test_delete_application_not_found(db):
    missing_id = 99999
    response = client.delete(f"/applications/{missing_id}")
    assert response.status_code == 404


def test_get_applications_filtered_by_status(db):
    rejected = make_application("Gama")
    rejected["status"] = "rejected"
    client.post("/applications", json=make_application("Acme"))
    client.post("/applications", json=make_application("Beta"))
    client.post("/applications", json=rejected)

    response = client.get("/applications", params={"status": "waiting"})

    assert response.status_code == 200
    assert len(response.json()) == 2
    for application in response.json():
        assert application["status"] == "waiting"


def test_get_applications_filtered_no_matches(db):
    client.post("/applications", json=make_application())

    response = client.get("/applications", params={"status": "offer"})

    assert response.status_code == 200
    assert response.json() == []


def test_get_applications_filtered_invalid_status(db):
    client.post("/applications", json=make_application())

    response = client.get("/applications", params={"status": "fail"})

    assert response.status_code == 422
