from pydantic import BaseModel, Field
from typing import Optional, Dict

class Student(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)  # MongoDB için _id
    student_id: str  # Backend’deki öğrenci ID’si
    subject_scores: Dict[str, float] = {}  # Konuya göre başarı endeksi

