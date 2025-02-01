from app.db.database import question_collection
from app.models.question import Question
from bson import ObjectId

# Tüm soruları getir
async def get_all_questions():
    questions = await question_collection.find().to_list(length=None)
    return questions

# Tek bir soruyu ID ile getir
async def get_question_by_id(question_id: str):
    question = await question_collection.find_one({"_id": ObjectId(question_id)})
    return question

# Yeni bir soru ekle
async def create_question(question: Question):
    result = await question_collection.insert_one(question.dict(by_alias=True))
    return str(result.inserted_id)

# Soruyu güncelle
async def update_question(question_id: str, data: dict):
    result = await question_collection.update_one(
        {"_id": ObjectId(question_id)}, {"$set": data}
    )
    return result.modified_count > 0

# Soruyu sil
async def delete_question(question_id: str):
    result = await question_collection.delete_one({"_id": ObjectId(question_id)})
    return result.deleted_count > 0
