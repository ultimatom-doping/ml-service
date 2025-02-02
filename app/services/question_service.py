from app.db.database import question_collection
from app.models.question import Question, QuestionUpdate
from bson import ObjectId
from fastapi import HTTPException

def serialize_document(doc):
    doc["_id"] = str(doc["_id"])
    return doc

# Tüm soruları getir
async def get_all_questions():
    questions = await question_collection.find().to_list(length=None)
    return [serialize_document(question) for question in questions]

# Tek bir soruyu ID ile getir
async def get_question_by_id(question_id: int):
    question = await question_collection.find_one({"question_id": question_id})
    if question:
        return serialize_document(question)
    return None

# Yeni bir soru ekle
async def create_question(question: Question):
    result = await question_collection.insert_one(question.dict(by_alias=True))
    return str(result.inserted_id)

# Soruyu güncelle
async def update_question(question_id: int, data: QuestionUpdate):
    update_data = {}

    if data.subject_id is not None:
        update_data["subject_id"] = data.subject_id

    if data.difficulty is not None:
        update_data["difficulty"] = data.difficulty

    if not update_data:
        raise HTTPException(status_code=400, detail="No valid update data provided")

    result = await question_collection.update_one(
        {"question_id": question_id}, {"$set": update_data}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Question not found")

    return True

# Soruyu sil
async def delete_question(question_id: int):
    result = await question_collection.delete_one({"question_id": question_id})
    return result.deleted_count > 0
