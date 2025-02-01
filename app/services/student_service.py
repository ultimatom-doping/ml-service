from app.db.database import student_collection
from app.models.student import Student
from bson import ObjectId

# Tüm öğrencileri getir
async def get_all_students():
    students = await student_collection.find().to_list(length=None)
    return students

# Tek bir öğrenciyi ID ile getir
async def get_student_by_id(student_id: str):
    student = await student_collection.find_one({"_id": ObjectId(student_id)})
    return student

# Yeni bir öğrenci ekle
async def create_student(student: Student):
    result = await student_collection.insert_one(student.dict(by_alias=True))
    return str(result.inserted_id)

# Öğrenciyi güncelle
async def update_student(student_id: str, data: dict):
    result = await student_collection.update_one(
        {"_id": ObjectId(student_id)}, {"$set": data}
    )
    return result.modified_count > 0

# Öğrenciyi sil
async def delete_student(student_id: str):
    result = await student_collection.delete_one({"_id": ObjectId(student_id)})
    return result.deleted_count > 0
