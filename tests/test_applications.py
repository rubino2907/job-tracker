from src.repositories import applications
import pytest

def test_add_applications(db):
    application = applications.add_application("Acme", "Backend Developer", "waiting", "2026-10-01")
    assert application["company"] == "Acme"

def test_get_applications(db):
        applications.add_application("Acme", "Backend Developer", "waiting", "2026-10-01")
        applications.add_application("Adidas", "Backend Developer", "waiting", "2026-10-01")
        apps = applications.get_applications()
        assert len(apps) == 2
        assert apps[1]["company"] == "Adidas" 