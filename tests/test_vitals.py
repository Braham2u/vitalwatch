from datetime import datetime, timezone
from fastapi.testclient import TestClient
from app.main import app
from app.storage import clear_all

client = TestClient(app)

def setup_function():
    clear_all()

def test_ingest_and_list_vitals():
    payload = {
        "patient_id": "p001",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "heart_rate_bpm": 78,
        "spo2_percent": 97,
        "systolic_mmHg": 120,
        "diastolic_mmHg": 80,
        "temperature_c": 36.7
    }

    r = client.post("/vitals", json=payload)
    assert r.status_code == 201

    r2 = client.get("/patients/p001/vitals")
    assert r2.status_code == 200
    data = r2.json()
    assert data["count"] == 1
    assert data["vitals"][0]["heart_rate_bpm"] == 78

def test_summary_endpoint():
    payload1 = {
        "patient_id": "p002",
        "timestamp": "2026-01-29T10:00:00+00:00",
        "heart_rate_bpm": 70,
        "spo2_percent": 98,
        "systolic_mmHg": 118,
        "diastolic_mmHg": 76,
        "temperature_c": 36.5
    }
    payload2 = {
        "patient_id": "p002",
        "timestamp": "2026-01-29T12:00:00+00:00",
        "heart_rate_bpm": 90,
        "spo2_percent": 95,
        "systolic_mmHg": 130,
        "diastolic_mmHg": 85,
        "temperature_c": 37.2
    }
    assert client.post("/vitals", json=payload1).status_code == 201
    assert client.post("/vitals", json=payload2).status_code == 201

    r = client.get("/patients/p002/summary")
    assert r.status_code == 200
    data = r.json()
    assert data["heart_rate"]["min"] == 70
    assert data["heart_rate"]["max"] == 90
