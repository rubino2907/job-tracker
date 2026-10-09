from src.repositories import applications
import pytest

def test_add_applications(db):
    application = applications.add_application(
        "Acme", "Backend Developer", "waiting", "2026-10-01"
    )
    assert application["company"] == "Acme"


def test_get_applications(db):
    applications.add_application("Acme", "Backend Developer", "waiting", "2026-10-01")
    applications.add_application("Adidas", "Backend Developer", "waiting", "2026-10-01")
    apps = applications.get_applications()
    assert len(apps) == 2
    assert apps[1]["company"] == "Adidas"


def test_get_application(db):
    applications.add_application("Acme", "Backend Developer", "waiting", "2026-10-01")
    applications.add_application("Adidas", "Backend Developer", "waiting", "2026-10-01")
    apps = applications.get_application(1)
    assert apps["company"] == "Acme"


def test_get_empty_applications(db):
    apps = applications.get_applications()
    assert len(apps) == 0


def test_add_application_invalid_status(db):
    with pytest.raises(ValueError):
        applications.add_application(
            company="acme",
            role="consultant",
            applied_date="22/07/2002",
            status="testFail",
        )
    apps = applications.get_applications()
    assert len(apps) == 0


def test_update_status_application_invalid_status(db):
    applications.add_application("Acme", "Backend Developer", "waiting", "2026-10-01")
    with pytest.raises(ValueError):
        applications.update_status_application(1, status="testFail")
    apps = applications.get_application(1)
    assert apps["status"] == "waiting"
