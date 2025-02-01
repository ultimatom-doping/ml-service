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
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def _get_pydantic_core_schema_(cls, _source_type, _handler):
        return {
            'type': 'custom',
            'custom_type_name': 'objectid',
            'encoding': 'str',
            'serialization': str,
            'validation': cls.validate,
        }

class Student(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    student_id: int
    subject_scores: Dict[str, float] = {}

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class StudentUpdate(BaseModel):
    subject_scores: Optional[Dict[str, float]] = None

    class Config:
        arbitrary_types_allowed = True