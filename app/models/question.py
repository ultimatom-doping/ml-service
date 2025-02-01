from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

class Question(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)  # MongoDB için _id
    question_id: str  # Backend’deki soru ID’si
    subject_id: str  # Sorunun ait olduğu konu
    total_attempts: int = 0  # Sorunun toplam kaç kez çözüldüğü
   
    difficulty_index: float = 0.0  # Sorunun zorluk endeksi (0-1 arası)