from pydantic import BaseModel, Field
from typing import Optional, Dict

class Student(BaseModel):
    student_id: int  # Backend’deki öğrenci ID’si
    subject_scores: Dict[str, float] = {}  # Konuya göre başarı endeksi

