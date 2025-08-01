# app/models/schemas.py

from pydantic import BaseModel

class ScanRequest(BaseModel):
    target: str
    scan_type: str


class ScanResult(BaseModel):
    scan_id: str
    status: str
    result_summary: str
