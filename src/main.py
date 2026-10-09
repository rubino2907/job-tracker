from fastapi import FastAPI

from src import database
from src.routers import applications

app = FastAPI()
database.init_db()
app.include_router(applications.router)
