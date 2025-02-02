from pydantic import BaseModel, Field, ConfigDict, GetJsonSchemaHandler
from bson import ObjectId
from typing import Optional
from pydantic.json_schema import JsonSchemaValue

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return handler.generate_schema(str)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler: GetJsonSchemaHandler) -> JsonSchemaValue:
        json_schema = handler(core_schema)
        json_schema.update(type="string")
        return json_schema

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

class Question(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    question_id: int
    subject_id: int
    difficulty: float = 0.0
    difficulty_cluster: int = 0
    confidence: float = 0.0
    correct_attempts: int = 0
    incorrect_attempts: int = 0
    empty_attempts: int = 0

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )

class QuestionUpdate(BaseModel):
    subject_id: Optional[int] = None
    difficulty: Optional[float] = None
    confidence: Optional[float] = None
    correct_attempts: Optional[int] = None
    incorrect_attempts: Optional[int] = None
    empty_attempts: Optional[int] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)
