from datetime import datetime
from pydantic import BaseModel, Field, conint, confloat

class VitalRecord(BaseModel):
    patient_id: str = Field(min_length=1, max_length=64)
    timestamp: datetime
    heart_rate_bpm: conint(ge=20, le=250)
    spo2_percent: conint(ge=0, le=100)
    systolic_mmHg: conint(ge=50, le=250)
    diastolic_mmHg: conint(ge=30, le=150)
    temperature_c: confloat(ge=30.0, le=45.0)
