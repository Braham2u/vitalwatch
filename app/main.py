from fastapi import FastAPI, HTTPException
from .models import VitalRecord
from .storage import add_vital, get_vitals

app = FastAPI(title="VitalWatch API", version="1.0.0")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/vitals", status_code=201)
def ingest_vitals(vital: VitalRecord):
    add_vital(vital)
    return {"message": "vitals ingested", "patient_id": vital.patient_id}

@app.get("/patients/{patient_id}/vitals")
def list_vitals(patient_id: str):
    vitals = get_vitals(patient_id)
    if not vitals:
        raise HTTPException(status_code=404, detail="No vitals found for patient")
    return {"patient_id": patient_id, "count": len(vitals), "vitals": vitals}

@app.get("/patients/{patient_id}/summary")
def vitals_summary(patient_id: str):
    vitals = get_vitals(patient_id)
    if not vitals:
        raise HTTPException(status_code=404, detail="No vitals found for patient")

    hr = [v.heart_rate_bpm for v in vitals]
    spo2 = [v.spo2_percent for v in vitals]
    temp = [float(v.temperature_c) for v in vitals]

    latest = vitals[0]
    return {
        "patient_id": patient_id,
        "latest_timestamp": latest.timestamp,
        "latest": latest,
        "heart_rate": {"min": min(hr), "max": max(hr), "avg": sum(hr)/len(hr)},
        "spo2": {"min": min(spo2), "max": max(spo2), "avg": sum(spo2)/len(spo2)},
        "temperature_c": {"min": min(temp), "max": max(temp), "avg": sum(temp)/len(temp)},
    }
