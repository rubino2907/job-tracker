from datetime import date

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.models import Status
from src.repositories import applications as repository


class NewApplication(BaseModel):
    company: str
    role: str
    status: Status
    applied_date: date
    notes: str | None = None


class StatusUpdate(BaseModel):
    status: Status


router = APIRouter(prefix="/applications", tags=["applications"])


@router.get("")
def get_applications(status: Status | None = None):
    return repository.get_applications(status)


@router.get("/{application_id}")
def get_application(application_id: int):
    try:
        return repository.get_application(application_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Application not found")


@router.post("")
def create_application(new_application: NewApplication):
    return repository.add_application(
        new_application.company,
        new_application.role,
        new_application.status,
        new_application.applied_date.isoformat(),
        new_application.notes,
    )


@router.patch("/{application_id}")
def update_application_status(application_id: int, body: StatusUpdate):
    try:
        return repository.update_status_application(application_id, body.status)
    except ValueError:
        raise HTTPException(status_code=404, detail="Application not found")


@router.delete("/{application_id}")
def delete_application(application_id: int):
    try:
        repository.delete_application(application_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Application not found")
    return {"message": "Application deleted"}
