from __future__ import annotations
from collections import defaultdict
from typing import Dict, List
from .models import VitalRecord

_vitals_by_patient: Dict[str, List[VitalRecord]] = defaultdict(list)

def add_vital(v: VitalRecord) -> None:
    _vitals_by_patient[v.patient_id].append(v)
    _vitals_by_patient[v.patient_id].sort(key=lambda x: x.timestamp, reverse=True)

def get_vitals(patient_id: str) -> List[VitalRecord]:
    return list(_vitals_by_patient.get(patient_id, []))

def clear_all() -> None:
    _vitals_by_patient.clear()
