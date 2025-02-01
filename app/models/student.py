from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional, Dict


class PyObjectId(ObjectId):
    @classmethod
    def _get_validators_(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def _modify_schema_(cls, field_schema):
        field_schema.update(type="string")

class Student(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    student_id: int
    subject_scores: Dict[str, float] = {}
    # Diğer alanlar...

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}