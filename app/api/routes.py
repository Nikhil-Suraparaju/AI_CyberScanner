# app/api/routes.py
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.services.nessus_api import create_scan, launch_scan, get_scan_results
from app.models.schemas import ScanRequest

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/scan", response_class=HTMLResponse)
async def scan(request: Request, target: str = Form(...), scan_type: str = Form(...)):
    try:
        # 1. Build request object (you could later use this for logging)
        scan_request = ScanRequest(target=target, scan_type=scan_type)

        # 2. Call Nessus service
        scan_id = create_scan(target)
        launch_scan(scan_id)
        result = get_scan_results(scan_id)

        # 3. Show result in the UI
        return templates.TemplateResponse("index.html", {
            "request": request,
            "scan_result": result,
            "target": target,
            "scan_type": scan_type
        })

    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": str(e)
        })
