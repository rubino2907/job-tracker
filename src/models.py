from enum import Enum

class Status(str, Enum):
    INTERVIEW_DONE = "interview_done"
    APPLIED = "applied"
    WAITING = "waiting"
    INTERVIEW_SCHEDULED = "interview_scheduled"
    OFFER = "offer"
    REJECTED = "rejected"
    ACCEPTED = "accepted"