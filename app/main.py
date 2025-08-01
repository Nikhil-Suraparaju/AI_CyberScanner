# app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.api.routes import router

app = FastAPI(
    title="Nessus Essentials - Scan Dashboard",
    description="A simple web UI to trigger and view Nessus network scans",
    version="1.0.0"
)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router)