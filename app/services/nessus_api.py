# app/services/nessus_api.py
import requests
import time
from app.models.schemas import ScanRequest, ScanResult

NESSUS_HOST = "https://localhost:8834"
HEADERS = {
    "X-ApiKeys": "accessKey=YOUR_ACCESS_KEY; secretKey=YOUR_SECRET_KEY",
    "Content-Type": "application/json"
}
VERIFY_SSL = False  # Only for localhost/testing

def create_scan(target: str) -> int:
    policy_id = get_basic_policy_id()
    scan_payload = {
        "uuid": policy_id,
        "settings": {
            "name": f"Scan-{target}",
            "text_targets": target,
            "policy_id": policy_id
        }
    }
    res = requests.post(f"{NESSUS_HOST}/scans", json=scan_payload, headers=HEADERS, verify=VERIFY_SSL)
    res.raise_for_status()
    return res.json()['scan']['id']

def launch_scan(scan_id: int):
    res = requests.post(f"{NESSUS_HOST}/scans/{scan_id}/launch", headers=HEADERS, verify=VERIFY_SSL)
    res.raise_for_status()
    return res.json()['scan_uuid']

def get_scan_results(scan_id: int) -> ScanResult:
    for _ in range(10):
        time.sleep(5)
        res = requests.get(f"{NESSUS_HOST}/scans/{scan_id}", headers=HEADERS, verify=VERIFY_SSL)
        res.raise_for_status()
        info = res.json()['info']
        if info['status'] == 'completed':
            summary = info.get('scan_start', '') + " → " + info.get('scan_end', '')
            return ScanResult(
                scan_id=str(scan_id),
                status=info['status'],
                result_summary=f"Scan completed. {summary}"
            )
    return ScanResult(
        scan_id=str(scan_id),
        status="timeout",
        result_summary="Scan did not complete in time."
    )

def get_basic_policy_id():
    res = requests.get(f"{NESSUS_HOST}/editor/policy/templates", headers=HEADERS, verify=VERIFY_SSL)
    res.raise_for_status()
    for policy in res.json()['templates']:
        if policy['name'] == 'basic':
            return policy['uuid']
    raise Exception("Basic policy template not found")
